import hmac
import json
import os
import re
import shutil
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Annotated, Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .artifacts import ArtifactStore
from .exporter import UgcPackageExporter
from .memory import DATABASE_SCHEMA_VERSION, MemoryStore
from .models import Goal, Risk
from .orchestrator import ApprovalError, Orchestrator
from .providers import DeterministicMockProvider, OpenAICompatibleProvider
from .research import ResearchSafetyError, SourceCollector

TENANT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
VALID_ROLES = frozenset({"viewer", "operator", "approver", "admin"})


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    tenant: str
    roles: frozenset[str]

    def __post_init__(self) -> None:
        if not self.subject.strip() or len(self.subject) > 320:
            raise ValueError("Principal subject must contain 1–320 characters")
        if not TENANT_PATTERN.fullmatch(self.tenant):
            raise ValueError("Tenant must contain 1–64 safe ASCII identifier characters")
        if not self.roles or not self.roles <= VALID_ROLES:
            raise ValueError("Principal contains missing or unsupported roles")


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    principals: dict[str, Principal]
    data_dir: Path
    default_mock: bool
    cors_origins: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "Settings":
        environment = os.getenv("TETRATIVE_ENV", "development").lower()
        principals: dict[str, Principal] = {}
        encoded = os.getenv("TETRATIVE_API_KEYS_JSON", "").strip()
        if encoded:
            try:
                configured = json.loads(encoded)
                if not isinstance(configured, dict):
                    raise TypeError("API key configuration must be an object")
                for secret, value in configured.items():
                    if not isinstance(secret, str) or not isinstance(value, dict):
                        raise TypeError("API key entries must map strings to objects")
                    principals[secret] = Principal(
                        subject=str(value["subject"]),
                        tenant=str(value["tenant"]),
                        roles=frozenset(value["roles"]),
                    )
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                raise RuntimeError("TETRATIVE_API_KEYS_JSON is invalid") from exc
        else:
            legacy = os.getenv("TETRATIVE_SERVER_API_KEY", "")
            if not legacy:
                legacy = "local-development-key"
            principals[legacy] = Principal(
                subject="local-admin",
                tenant="default",
                roles=frozenset({"admin"}),
            )
        if environment == "production" and any(len(secret) < 24 for secret in principals):
            raise RuntimeError("Production bearer keys must contain at least 24 characters")
        data_dir = Path(os.getenv("TETRATIVE_DATA_DIR", ".tetrative")).resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
        origins = tuple(filter(None, os.getenv("TETRATIVE_CORS_ORIGINS", "").split(",")))
        return cls(
            environment=environment,
            principals=principals,
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


class ResearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2_000)
    urls: list[str] = Field(min_length=1, max_length=10)


def _migrate_legacy_default_tenant(settings: Settings) -> None:
    """Move v0.3 single-tenant state once, without merging or overwriting data."""
    if not any(principal.tenant == "default" for principal in settings.principals.values()):
        return
    target = settings.data_dir / "tenants" / "default"
    target.mkdir(parents=True, exist_ok=True)
    legacy_database = settings.data_dir / "memory.db"
    target_database = target / "memory.db"
    if legacy_database.exists() and not target_database.exists():
        os.replace(legacy_database, target_database)
        for suffix in ("-wal", "-shm"):
            legacy_sidecar = Path(f"{legacy_database}{suffix}")
            if legacy_sidecar.exists():
                os.replace(legacy_sidecar, Path(f"{target_database}{suffix}"))
    legacy_artifacts = settings.data_dir / "artifacts"
    target_artifacts = target / "artifacts"
    if legacy_artifacts.is_dir() and not target_artifacts.exists():
        shutil.move(str(legacy_artifacts), str(target_artifacts))


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    _migrate_legacy_default_tenant(settings)
    app = FastAPI(
        title="Tetrative Agentic OS",
        version="0.4.0",
        description="Human-governed orchestration for grounded venture and UGC production.",
    )
    app.state.settings = settings
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.cors_origins),
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        )

    @app.middleware("http")
    async def request_trace(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", "")
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", request_id):
            request_id = str(uuid4())
        request.state.request_id = request_id
        started = time.monotonic()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        principal = getattr(request.state, "principal", None)
        event = {
            "kind": "http_request",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round((time.monotonic() - started) * 1000, 2),
            "subject": principal.subject if principal else None,
            "tenant": principal.tenant if principal else None,
        }
        print(json.dumps(event, sort_keys=True), flush=True)
        return response

    def authenticate(
        request: Request,
        authorization: Annotated[str | None, Header()] = None,
    ) -> Principal:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Bearer API key required")
        supplied = authorization.removeprefix("Bearer ")
        principal = next(
            (
                candidate
                for secret, candidate in settings.principals.items()
                if hmac.compare_digest(supplied, secret)
            ),
            None,
        )
        if principal is None:
            raise HTTPException(status_code=403, detail="Invalid API key")
        request.state.principal = principal
        return principal

    def require(*roles: str):
        def authorize(principal: Annotated[Principal, Depends(authenticate)]) -> Principal:
            if "admin" not in principal.roles and principal.roles.isdisjoint(roles):
                raise HTTPException(status_code=403, detail="Principal lacks the required role")
            return principal

        return authorize

    viewer = require("viewer", "operator", "approver")
    operator = require("operator")
    approver = require("approver")

    def tenant_resources(principal: Principal) -> tuple[Path, ArtifactStore]:
        root = settings.data_dir / "tenants" / principal.tenant
        root.mkdir(parents=True, exist_ok=True)
        return root / "memory.db", ArtifactStore(root / "artifacts")

    def provider(mock: bool | None):
        use_mock = settings.default_mock if mock is None else mock
        return DeterministicMockProvider() if use_mock else OpenAICompatibleProvider.from_env()

    def evidence_context(artifacts: ArtifactStore, artifact_id: str) -> str:
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
        return {
            "status": "ok",
            "environment": settings.environment,
            "database_schema": str(DATABASE_SCHEMA_VERSION),
        }

    @app.get("/api/v1/session", tags=["identity"])
    def session(principal: Annotated[Principal, Depends(viewer)]) -> dict:
        return asdict(principal)

    @app.get("/api/v1/runs", tags=["runs"])
    def list_runs(
        principal: Annotated[Principal, Depends(viewer)],
        limit: int = Query(default=50, ge=1, le=200),
    ) -> list[dict]:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            return memory.list_checkpoints(limit=limit)
        finally:
            memory.close()

    @app.post("/api/v1/runs", tags=["runs"])
    def create_run(request: RunCreate, principal: Annotated[Principal, Depends(operator)]) -> dict:
        if settings.environment == "production" and request.auto_approve:
            raise HTTPException(status_code=403, detail="Auto-approval is disabled in production")
        database_path, artifacts = tenant_resources(principal)
        constraints = list(request.constraints)
        if request.research_artifact_id:
            try:
                constraints.append(evidence_context(artifacts, request.research_artifact_id))
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

    @app.get("/api/v1/runs/{run_id}", tags=["runs"])
    def get_run(run_id: str, principal: Annotated[Principal, Depends(viewer)]) -> dict:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            checkpoint = memory.load_checkpoint(run_id)
            if checkpoint is None:
                raise HTTPException(status_code=404, detail="Run not found")
            return {"run_id": run_id, **checkpoint, "events": memory.events(run_id)}
        finally:
            memory.close()

    @app.post("/api/v1/runs/{run_id}/approve", tags=["runs"])
    def approve_run(
        run_id: str,
        request: ApprovalRequest,
        principal: Annotated[Principal, Depends(approver)],
        mock: bool | None = None,
    ) -> dict:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            result = Orchestrator(provider(mock), memory).resume(
                run_id, request.artifact_hash, approver=principal.subject
            )
            return result.to_dict()
        except ApprovalError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        finally:
            memory.close()

    @app.post("/api/v1/research", tags=["research"])
    def collect_research(
        request: ResearchRequest,
        principal: Annotated[Principal, Depends(operator)],
    ) -> dict:
        _, artifacts = tenant_resources(principal)
        try:
            bundle = SourceCollector(artifacts).collect(request.question, request.urls)
            return asdict(bundle)
        except (ResearchSafetyError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    @app.post("/api/v1/runs/{run_id}/exports/ugc", tags=["exports"])
    def export_ugc(run_id: str, principal: Annotated[Principal, Depends(operator)]) -> dict:
        database_path, artifacts = tenant_resources(principal)
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

    @app.get("/api/v1/artifacts/{artifact_id}", tags=["artifacts"])
    def download_artifact(
        artifact_id: str,
        principal: Annotated[Principal, Depends(viewer)],
    ) -> Response:
        _, artifacts = tenant_resources(principal)
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
