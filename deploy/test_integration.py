#!/usr/bin/env python3
"""
OMEGA MEDIA OS v1.0 — INTEGRATION DEMONSTRATION
End-to-end test: User request → Orchestrator → Agent activation → Memory update → Output
"""

import sys
import time
from pathlib import Path

# Ensure project is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agents.orchestrator import MasterOrchestrator, OmegaState
from core.memory.interface import MemoryBank
from core.analytics.module import AnalyticsSchema


def run_demo():
    print("=" * 60)
    print("OMEGA MEDIA OS v1.0 — INTEGRATION DEMONSTRATION")
    print("Branch: arena/01a029a2-agentic-ugc")
    print("Thesis: One strategic mind → many specialized cognitive agents → ... → continuously improving intelligence")
    print("=" * 60)

    # Initialize components
    orchestrator = MasterOrchestrator()
    memory = MemoryBank()
    analytics = AnalyticsSchema(memory_bank=memory)

    print(f"\n[INIT] Master Orchestrator: {orchestrator.name} v{orchestrator.version}")
    print(f"[INIT] Memory Banks Active: {', '.join(memory.BANKS)}")
    print(f"[INIT] Analytics Engine: Active")
    print(f"[INIT] Production State Machine: {len(OmegaState.STATES)} states, {len(OmegaState.VALID_TRANSITIONS)} transition rules")

    # Example 1: Content strategy request
    print("\n" + "-" * 60)
    print("DEMO 1: Content Strategy Activation (Filmmaker Role)")
    print("-" * 60)

    request_text = (
        "Design a YouTube documentary series about AI cinema production. "
        "It must connect to a digital product for independent filmmakers. "
        "The series should avoid AI slop and maintain cinematic identity."
    )

    start_time = time.time()
    result = orchestrator.receive_request(request_text, role_hint="filmmaker")
    activation_time = time.time() - start_time

    if result.get("status") == "ACTIVATED":
        print(f"[ACTIVATED] Agent: {result['assigned_agent']} in {activation_time:.2f}s")
        print(f"[PACKET] Size: {result['packet_size_bytes']} bytes (max: 10240)")
        print(f"[PACKET] Pollution: {result['pollution_score']:.2f} (max: 0.30)")
        print(f"[PACKET] Failure Pin: {result['failure_pin_present']}")
        print(f"[PACKET] Thesis Check: {result['thesis_check']}")
        print(f"[PACKET] State: {result['current_state']} → {result['target_state']}")

        # Execute agent
        execution = orchestrator.execute_agent(result["task_id"])
        print(f"[EXECUTION] Agent executed in {execution.get('simulated_output', {}).get('execution_time_seconds', 'N/A')}s")
        print(f"[EXECUTION] Memory updates planned: {len(execution.get('simulated_output', {}).get('memory_updates_planned', []))}")

    # Example 2: Analytics event recording
    print("\n" + "-" * 60)
    print("DEMO 2: Analytics Event → Memory Integration")
    print("-" * 60)

    event = analytics.record_event(
        event_type="content_view",
        agent_id="OMEGA-C2",
        task_id="demo-task-42",
        channel_id="OMEGA-DOCUMENTARY",
        content_id="demo-content-1",
        metrics={"retention_30s": 0.62, "watch_time_total": 240},
        dimensions={"device": "mobile", "region": "NA"},
        quality_indicators={"omega_score": 0.72, "truth_score": 0.85},
    )
    print(f"[EVENT] Recorded: {event['event_type']} (ID: {event['event_id'][:8]}...)")
    print(f"[EVENT] Metrics: {event['metrics']}")
    print(f"[EVENT] Memory updates: {event['memory_updates']}")

    # Example 3: Memory read
    print("\n" + "-" * 60)
    print("DEMO 3: Memory Read (All 6 Banks)")
    print("-" * 60)

    for bank in memory.BANKS:
        results = memory.read_memory(bank, max_results=3)
        print(f"[MEMORY] {bank}: {len(results)} entries (latest: {results[0]['entry_id'][:8] if results else 'none'}...)")

    # Example 4: State transition validation
    print("\n" + "-" * 60)
    print("DEMO 4: State Machine Validation")
    print("-" * 60)

    valid_transitions = [
        ("OBSERVE", "CAPTURE"),
        ("CAPTURE", "CLASSIFY"),
        ("CLASSIFY", "RESEARCH"),
        ("RESEARCH", "SYNTHESIZE"),
        ("SYNTHESIZE", "HYPOTHESIZE"),
    ]
    for current, target in valid_transitions:
        ok = OmegaState.can_transition(current, target)
        gate = OmegaState.requires_gate(current, target)
        print(f"[STATE] {current} → {target}: VALID={ok} | GATE={gate}")

    # Example 5: Quality engine calculation
    print("\n" + "-" * 60)
    print("DEMO 5: Quality Engine (OMEGA Score)")
    print("-" * 60)

    c, t, p, b, r = 0.85, 0.92, 0.88, 0.75, 0.12
    omega_score = c * t * p * b * (1 - r)
    print(f"[QUALITY] C={c}, T={t}, P={p}, B={b}, R={r}")
    print(f"[QUALITY] OMEGA SCORE = {omega_score:.3f}")
    print(f"[QUALITY] Threshold: PUBLISH (>0.6) = {omega_score > 0.6}")
    print(f"[QUALITY] Scale Fast (>0.8 + R<0.2) = {omega_score > 0.8 and r < 0.2}")

    # Final system status
    print("\n" + "=" * 60)
    print("DEMO COMPLETE — OMEGA v1.0 OPERATIONAL")
    print("=" * 60)
    status = orchestrator.get_system_status()
    print(f"Status: {status['active_tasks']} active tasks | Registry: {status['registry_path']}")
    print(f"Non-negotiable rules: {status['non_negotiable_rules_active']} active")
    print(f"Benchmark targets: Activation <10s | SGNL <5s | Red Team <1h | Evolution <4h")
    print("\nNext actions (Day 1 protocol): Initialize full agent registry → Build first context packets → Execute red team review → Write failure memory → Repeat.")


if __name__ == "__main__":
    run_demo()
