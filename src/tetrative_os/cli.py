from __future__ import annotations

import argparse
import json
from pathlib import Path

from .memory import MemoryStore
from .models import Goal, Risk
from .orchestrator import Orchestrator
from .providers import DeterministicMockProvider, OpenAICompatibleProvider


def parser() -> argparse.ArgumentParser:
    app = argparse.ArgumentParser(prog="tetrative", description="Run the Tetrative Agentic OS")
    app.add_argument("objective", nargs="?", help="High-level objective (omit with --resume)")
    app.add_argument("--domain", choices=("meta", "ugc", "venture", "ecosystem"), default="meta")
    app.add_argument("--resume", metavar="RUN_ID", help="Resume a durable human-gate checkpoint")
    app.add_argument("--approve", metavar="SHA256", help="Digest of the exact artifact being approved")
    app.add_argument("--approver", help="Authenticated human identity recorded in the audit log")
    app.add_argument("--audience", default="unspecified")
    app.add_argument("--constraint", action="append", default=[])
    app.add_argument("--metric", action="append", default=[])
    app.add_argument("--risk", choices=[x.value for x in Risk], default="medium")
    app.add_argument("--mock", action="store_true", help="Use deterministic offline model")
    app.add_argument("--auto-approve", action="store_true", help="Pass human gates (demo/CI only)")
    app.add_argument("--output", default="run.json")
    app.add_argument("--memory", default=".tetrative/memory.db")
    return app


def main() -> None:
    args = parser().parse_args()
    provider = DeterministicMockProvider() if args.mock else OpenAICompatibleProvider.from_env()
    memory = MemoryStore(args.memory)
    try:
        orchestrator = Orchestrator(provider, memory)
        if args.resume:
            if not args.approve or not args.approver:
                parser().error("--resume requires --approve and --approver")
            result = orchestrator.resume(args.resume, args.approve, approver=args.approver)
        else:
            if not args.objective:
                parser().error("objective is required unless --resume is used")
            goal = Goal(
                args.objective, args.domain, args.audience, args.constraint, args.metric, Risk(args.risk)
            )
            result = orchestrator.run(goal, auto_approve=args.auto_approve)
        Path(args.output).write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
        print(f"{result.status}: {result.run_id} -> {args.output}")
        print(f"quality={result.metrics['average_quality']:.2f}")
        if result.approval_required:
            print(f"approval_hash={result.approval_required['artifact_hash']}")
    finally:
        memory.close()


if __name__ == "__main__":
    main()
