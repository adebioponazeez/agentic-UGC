# ADR-0001: retain a local-first orchestration kernel

**Status:** Accepted · **Date:** 2026-08-22

LangGraph, Temporal, Pydantic AI, CrewAI, and observability platforms solve valuable portions of the
problem but can couple domain behavior to framework semantics. Keep deterministic domain
orchestration in a small provider-neutral kernel and add adapters for durable workflows, schemas,
retrieval, tools, and observability.

The MVP remains inspectable and dependency-light. It must not pretend local SQLite is distributed
infrastructure. Adapter contract tests are mandatory before replacement.
