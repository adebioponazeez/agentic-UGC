from __future__ import annotations

import hmac
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .artifacts import ArtifactStore
from .exporter import UgcPackageExporter
from .memory import MemoryStore
from .models import Goal, Risk
from .orchestrator import ApprovalError, Orchestrator
from .providers import DeterministicMockProvider, OpenAICompatibleProvider
from .research import ResearchSafetyError, SourceCollector


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    api_key: str
    data_dir: Path
    default_mock: bool
    cors_origins: tuple[str, ...]

    @classmethod
    def from_env(cls) -> Settings:
        environment = os.getenv("TETRATIVE_ENV", "development").lower()
        api_key = os.getenv("TETRATIVE_SERVER_API_KEY", "")
        if environment == "production" and len(api_key) < 24:
            raise RuntimeError("Production requires TETRATIVE_SERVER_API_KEY with at least 24 characters")
        if not api_key:
            api_key = "local-development-key"
        data_dir = Path(os.getenv("TETRATIVE_DATA_DIR", ".tetrative")).resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
        origins = tuple(filter(None, os.getenv("TETRATIVE_CORS_ORIGINS", "").split(",")))
        return cls(
            environment=environment,
            api_key=api_key,
            data_dir=data_dir,
            default_mock=os.getenv("TETRATIVE_DEFAULT_MOCK", "true").lower() == "true",
            cors_origins=origins,
        )


class RunCreate(BaseModel):
    objective: str = Field(min_length=1, max_length=10_000)
    domain: Literal["meta", "ugc", "venture", "ecosystem"] = "ecosystem"
    audience: str = Field(default="unspecified", max_length=2_000)
    constraints: list[str] = Field(default_factory=list, max_length=100)
    success_metrics: list[str] = Field(default_factory=list, max_length=100)
    risk: Risk = Risk.MEDIUM
    research_artifact_id: str | None = None
    auto_approve: bool = False
    mock: bool | None = None


class ApprovalRequest(BaseModel):
    artifact_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    approver: str = Field(min_length=1, max_length=320)


class ResearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2_000)
    urls: list[str] = Field(min_length=1, max_length=10)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(
        title="Tetrative Agentic OS",
        version="0.3.0",
        description="Human-governed orchestration for grounded venture and UGC production.",
    )
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.cors_origins),
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type"],
        )

    database_path = settings.data_dir / "memory.db"
    artifacts = ArtifactStore(settings.data_dir / "artifacts")

    def authorize(authorization: Annotated[str | None, Header()] = None) -> None:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Bearer API key required")
        supplied = authorization.removeprefix("Bearer ")
        if not hmac.compare_digest(supplied, settings.api_key):
            raise HTTPException(status_code=403, detail="Invalid API key")

    auth = Depends(authorize)

    def provider(mock: bool | None):
        use_mock = settings.default_mock if mock is None else mock
        return DeterministicMockProvider() if use_mock else OpenAICompatibleProvider.from_env()

    def evidence_context(artifact_id: str) -> str:
        artifact, content = artifacts.get(artifact_id)
        if artifact.kind != "research.bundle.v1":
            raise ValueError("Artifact is not a research bundle")
        bundle = json.loads(content)
        blocks = [
            f"RESEARCH_BUNDLE_ARTIFACT_ID: {artifact_id}",
            "SOURCE-GROUNDED EVIDENCE. Cite [S#] for factual claims; label unsupported claims as assumptions.",
        ]
        for source in bundle.get("sources", []):
            blocks.append(
                f"{source['citation_id']} {source['title']}\nURL: {source['final_url']}\n"
                f"Fetched: {source['fetched_at']}\n{source['text']}"
            )
        return "\n\n".join(blocks)[:40_000]

    @app.get("/healthz", tags=["operations"])
    def health() -> dict[str, str]:
        memory = MemoryStore(database_path)
        try:
            return {
                "status": "ok",
                "environment": settings.environment,
                "database_schema": str(memory.schema_version),
            }
        finally:
            memory.close()

    @app.get("/api/v1/runs", dependencies=[auth], tags=["runs"])
    def list_runs(limit: int = Query(default=50, ge=1, le=200)) -> list[dict]:
        memory = MemoryStore(database_path)
        try:
            return memory.list_checkpoints(limit=limit)
        finally:
            memory.close()

    @app.post("/api/v1/runs", dependencies=[auth], tags=["runs"])
    def create_run(request: RunCreate) -> dict:
        if settings.environment == "production" and request.auto_approve:
            raise HTTPException(status_code=403, detail="Auto-approval is disabled in production")
        constraints = list(request.constraints)
        if request.research_artifact_id:
            try:
                constraints.append(evidence_context(request.research_artifact_id))
            except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc
        try:
            goal = Goal(
                objective=request.objective,
                domain=request.domain,
                audience=request.audience,
                constraints=constraints,
                success_metrics=request.success_metrics,
                risk=request.risk,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        memory = MemoryStore(database_path)
        try:
            result = Orchestrator(provider(request.mock), memory).run(
                goal, auto_approve=request.auto_approve
            )
            return result.to_dict()
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        finally:
            memory.close()

    @app.get("/api/v1/runs/{run_id}", dependencies=[auth], tags=["runs"])
    def get_run(run_id: str) -> dict:
        memory = MemoryStore(database_path)
        try:
            checkpoint = memory.load_checkpoint(run_id)
            if checkpoint is None:
                raise HTTPException(status_code=404, detail="Run not found")
            return {"run_id": run_id, **checkpoint, "events": memory.events(run_id)}
        finally:
            memory.close()

    @app.post("/api/v1/runs/{run_id}/approve", dependencies=[auth], tags=["runs"])
    def approve_run(run_id: str, request: ApprovalRequest, mock: bool | None = None) -> dict:
        memory = MemoryStore(database_path)
        try:
            result = Orchestrator(provider(mock), memory).resume(
                run_id, request.artifact_hash, approver=request.approver
            )
            return result.to_dict()
        except ApprovalError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        finally:
            memory.close()

    @app.post("/api/v1/research", dependencies=[auth], tags=["research"])
    def collect_research(request: ResearchRequest) -> dict:
        try:
            bundle = SourceCollector(artifacts).collect(request.question, request.urls)
            return asdict(bundle)
        except (ResearchSafetyError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    @app.post("/api/v1/runs/{run_id}/exports/ugc", dependencies=[auth], tags=["exports"])
    def export_ugc(run_id: str) -> dict:
        memory = MemoryStore(database_path)
        try:
            checkpoint = memory.load_checkpoint(run_id)
            if checkpoint is None:
                raise HTTPException(status_code=404, detail="Run not found")
            try:
                return asdict(UgcPackageExporter(artifacts).export(run_id, checkpoint))
            except ValueError as exc:
                raise HTTPException(status_code=409, detail=str(exc)) from exc
        finally:
            memory.close()

    @app.get("/api/v1/artifacts/{artifact_id}", dependencies=[auth], tags=["artifacts"])
    def download_artifact(artifact_id: str) -> Response:
        try:
            artifact, content = artifacts.get(artifact_id)
        except (FileNotFoundError, ValueError):
            raise HTTPException(status_code=404, detail="Artifact not found")
        return Response(
            content,
            media_type=artifact.content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{artifact.kind}-{artifact.id}"',
                "ETag": f'"{artifact.sha256}"',
            },
        )

    web = Path(__file__).with_name("web")
    app.mount("/assets", StaticFiles(directory=web), name="assets")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(web / "index.html")

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(
        "tetrative_os.api:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
