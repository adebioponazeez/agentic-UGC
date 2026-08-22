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
from .autonomy import ActionProposal, AutonomyController
from .exporter import UgcPackageExporter
from .memory import DATABASE_SCHEMA_VERSION, MemoryStore
from .models import Goal, Risk
from .orchestrator import ApprovalError, Orchestrator
from .outcomes import (
    AuthorityEnvelope,
    Direction,
    Metric,
    Observation,
    OutcomeStatus,
    StrategicBet,
    StrategicOutcome,
    StrategicOutcomeEngine,
    observation_from_dict,
    outcome_from_dict,
    outcome_to_dict,
)
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
    domain: Literal["meta", "ugc", "venture", "outcome", "ecosystem"] = "ecosystem"
    outcome_id: str | None = None
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


class MetricInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    unit: str = Field(min_length=1, max_length=100)
    baseline: float
    target: float
    direction: Direction = Direction.MAXIMIZE


class BetInput(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    owner: str = Field(min_length=1, max_length=320)
    hypothesis: str = Field(min_length=1, max_length=4_000)
    expected_impact: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    requested_cost_minor: int = Field(ge=0)
    reversible: bool = True
    kill_criterion: str = Field(min_length=1, max_length=2_000)
    evidence: list[str] = Field(default_factory=list, max_length=50)


class AuthorityInput(BaseModel):
    allowed_tools: list[str] = Field(default_factory=list, max_length=100)
    max_risk: Literal["low", "medium", "high", "critical"] = "low"
    total_spend_minor: int = Field(default=0, ge=0)
    approval_spend_threshold_minor: int = Field(default=0, ge=0)
    max_actions_per_day: int = Field(default=20, ge=1, le=10_000)
    protected_categories: list[str] | None = None
    kill_switch: bool = False


class OutcomeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    north_star: str = Field(min_length=1, max_length=4_000)
    metric: MetricInput
    capital_budget_minor: int = Field(ge=0)
    guardrails: list[str] = Field(min_length=1, max_length=100)
    bets: list[BetInput] = Field(min_length=1, max_length=100)
    authority: AuthorityInput
    deadline_days: int = Field(default=1460, ge=1, le=3650)


class ObservationCreate(BaseModel):
    metric_name: str = Field(min_length=1, max_length=200)
    value: float
    note: str = Field(min_length=1, max_length=4_000)
    evidence_artifact_id: str | None = None


class KillSwitchRequest(BaseModel):
    enabled: bool
    reason: str = Field(min_length=1, max_length=2_000)


class ActionCreate(BaseModel):
    tool: str = Field(min_length=1, max_length=300)
    category: str = Field(min_length=1, max_length=100)
    risk: Literal["low", "medium", "high", "critical"]
    estimated_spend_minor: int = Field(ge=0)
    reversible: bool
    external_effect: bool
    expected_effect: str = Field(min_length=1, max_length=4_000)
    rollback: str = Field(default="", max_length=4_000)
    idempotency_key: str | None = Field(default=None, max_length=300)


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
        title="Tetrative Strategic Outcome OS · Version 220",
        version="220.0.0",
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

    def load_outcome(memory: MemoryStore, outcome_id: str) -> tuple[StrategicOutcome, dict]:
        record = memory.get_outcome(outcome_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Strategic outcome not found")
        return outcome_from_dict(record["payload"]["contract"]), record

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

    @app.post("/api/v220/outcomes", tags=["outcomes"])
    def create_outcome(
        request: OutcomeCreate,
        principal: Annotated[Principal, Depends(operator)],
    ) -> dict:
        database_path, _ = tenant_resources(principal)
        authority_data = request.authority.model_dump()
        if authority_data["protected_categories"] is None:
            authority_data.pop("protected_categories")
        try:
            outcome = StrategicOutcome(
                title=request.title,
                north_star=request.north_star,
                owner=principal.subject,
                metric=Metric(**request.metric.model_dump()),
                capital_budget_minor=request.capital_budget_minor,
                guardrails=request.guardrails,
                bets=[StrategicBet(**item.model_dump()) for item in request.bets],
                authority=AuthorityEnvelope(**authority_data),
                deadline_days=request.deadline_days,
            )
            plan = StrategicOutcomeEngine().plan(outcome)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        payload = {"contract": outcome_to_dict(outcome), "plan": asdict(plan)}
        memory = MemoryStore(database_path)
        try:
            memory.save_outcome(outcome.id, outcome.status.value, payload)
            memory.record_outcome_decision(
                str(uuid4()), outcome.id, "initial_plan", asdict(plan)
            )
            return {"outcome": payload["contract"], "plan": payload["plan"]}
        finally:
            memory.close()

    @app.get("/api/v220/outcomes", tags=["outcomes"])
    def list_outcomes(
        principal: Annotated[Principal, Depends(viewer)],
        limit: int = Query(default=50, ge=1, le=200),
    ) -> list[dict]:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            return memory.list_outcomes(limit)
        finally:
            memory.close()

    @app.get("/api/v220/outcomes/{outcome_id}", tags=["outcomes"])
    def get_outcome(
        outcome_id: str,
        principal: Annotated[Principal, Depends(viewer)],
    ) -> dict:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            _, record = load_outcome(memory, outcome_id)
            return {
                **record,
                "observations": memory.outcome_observations(outcome_id),
                "decisions": memory.outcome_decisions(outcome_id),
                "actions": memory.outcome_actions(outcome_id),
            }
        finally:
            memory.close()

    @app.post("/api/v220/outcomes/{outcome_id}/observations", tags=["outcomes"])
    def observe_outcome(
        outcome_id: str,
        request: ObservationCreate,
        principal: Annotated[Principal, Depends(operator)],
    ) -> dict:
        database_path, artifacts = tenant_resources(principal)
        if request.evidence_artifact_id:
            try:
                artifacts.get(request.evidence_artifact_id)
            except (FileNotFoundError, ValueError):
                raise HTTPException(status_code=422, detail="Evidence artifact not found in tenant")
        memory = MemoryStore(database_path)
        try:
            outcome, record = load_outcome(memory, outcome_id)
            try:
                observation = Observation(
                    outcome_id=outcome_id,
                    metric_name=request.metric_name,
                    value=request.value,
                    note=request.note,
                    evidence_artifact_id=request.evidence_artifact_id,
                )
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc
            memory.add_observation(asdict(observation))
            response: dict = {"observation": asdict(observation), "recalibration": None}
            if observation.metric_name == outcome.metric.name:
                observations = [
                    observation_from_dict(item)
                    for item in memory.outcome_observations(outcome_id)
                ]
                decision = StrategicOutcomeEngine().recalibrate(outcome, observations)
                if outcome.authority.kill_switch:
                    outcome.paused_from_status = decision.status
                    outcome.status = OutcomeStatus.PAUSED
                else:
                    outcome.status = decision.status
                record["payload"]["contract"] = outcome_to_dict(outcome)
                memory.save_outcome(outcome.id, outcome.status.value, record["payload"])
                memory.record_outcome_decision(
                    decision.id, outcome.id, "recalibration", asdict(decision)
                )
                response["recalibration"] = asdict(decision)
            return response
        finally:
            memory.close()

    @app.post("/api/v220/outcomes/{outcome_id}/kill-switch", tags=["outcomes"])
    def set_outcome_kill_switch(
        outcome_id: str,
        request: KillSwitchRequest,
        principal: Annotated[Principal, Depends(approver)],
    ) -> dict:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            outcome, record = load_outcome(memory, outcome_id)
            outcome.authority.kill_switch = request.enabled
            if request.enabled:
                if outcome.status is not OutcomeStatus.PAUSED:
                    outcome.paused_from_status = outcome.status
                outcome.status = OutcomeStatus.PAUSED
            else:
                outcome.status = outcome.paused_from_status or OutcomeStatus.ACTIVE
                outcome.paused_from_status = None
            record["payload"]["contract"] = outcome_to_dict(outcome)
            memory.save_outcome(outcome.id, outcome.status.value, record["payload"])
            decision = {
                "enabled": request.enabled,
                "reason": request.reason,
                "actor": principal.subject,
                "status": outcome.status.value,
            }
            memory.record_outcome_decision(
                str(uuid4()), outcome.id, "kill_switch", decision
            )
            return decision
        finally:
            memory.close()

    @app.post("/api/v220/outcomes/{outcome_id}/actions/authorize", tags=["outcomes"])
    def authorize_action(
        outcome_id: str,
        request: ActionCreate,
        principal: Annotated[Principal, Depends(operator)],
    ) -> dict:
        database_path, _ = tenant_resources(principal)
        memory = MemoryStore(database_path)
        try:
            outcome, _ = load_outcome(memory, outcome_id)
            previous = memory.outcome_actions(outcome_id)
            if request.idempotency_key:
                duplicate = next(
                    (
                        item["payload"]
                        for item in previous
                        if item["payload"]["proposal"].get("idempotency_key")
                        == request.idempotency_key
                    ),
                    None,
                )
                if duplicate is not None:
                    original = duplicate["proposal"]
                    requested = request.model_dump()
                    if any(original.get(key) != value for key, value in requested.items()):
                        raise HTTPException(
                            status_code=409,
                            detail="Idempotency key was already used for a different action proposal",
                        )
                    return {**duplicate, "replayed": True}
            spent = sum(
                item["payload"]["proposal"]["estimated_spend_minor"]
                for item in previous
                if item["authorization"] == "allow"
            )
            proposal = ActionProposal(outcome_id=outcome_id, **request.model_dump())
            decision = AutonomyController().decide(
                proposal,
                outcome.authority,
                spent_minor=spent,
                actions_today=len(previous),
            )
            payload = {
                "proposal": asdict(proposal),
                "decision": decision.to_dict(),
                "authorized_by": principal.subject,
                "replayed": False,
            }
            memory.record_action_decision(
                proposal.id, outcome_id, decision.authorization.value, payload
            )
            return payload
        finally:
            memory.close()

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
        linked_outcome: StrategicOutcome | None = None
        if request.outcome_id:
            outcome_memory = MemoryStore(database_path)
            try:
                linked_outcome, _ = load_outcome(outcome_memory, request.outcome_id)
            finally:
                outcome_memory.close()
            if linked_outcome.authority.kill_switch:
                raise HTTPException(
                    status_code=423,
                    detail="Strategic outcome kill switch is active",
                )
            constraints.append(
                "STRATEGIC_OUTCOME_CONTRACT: "
                f"id={linked_outcome.id}; north_star={linked_outcome.north_star}; "
                f"metric={linked_outcome.metric.name}; baseline={linked_outcome.metric.baseline}; "
                f"target={linked_outcome.metric.target} {linked_outcome.metric.unit}; "
                f"guardrails={linked_outcome.guardrails}. Agent artifacts do not count as metric progress."
            )
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
            if linked_outcome is not None:
                memory.record_outcome_decision(
                    str(uuid4()),
                    linked_outcome.id,
                    "agent_run",
                    {
                        "run_id": result.run_id,
                        "domain": goal.domain,
                        "status": result.status,
                        "note": "Agent output is advisory evidence, not observed outcome progress.",
                    },
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
