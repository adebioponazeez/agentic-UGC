#!/usr/bin/env python3
"""
OMEGA MEDIA OS v1.0 — MASTER ORCHESTRATOR (OMEGA-0)
Core routing, context packet construction, state machine management,
and agent activation protocol.
"""

import json
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

# Import local modules (will be implemented as files grow)
try:
    from core.memory.schema import MemoryBank, MemoryReadResult, MemoryWriteResult
except ImportError:
    MemoryBank = str
    MemoryReadResult = Dict
    MemoryWriteResult = Dict


class OmegaState:
    """Production state machine — persistent, observable, recoverable."""
    STATES = [
        "OBSERVE", "CAPTURE", "CLASSIFY", "CONNECT", "RESEARCH",
        "SYNTHESIZE", "HYPOTHESIZE", "CHALLENGE", "PRIORITIZE",
        "DESIGN", "SIMULATE", "PRODUCE", "VERIFY", "PACKAGE",
        "DISTRIBUTE", "MEASURE", "DIAGNOSE", "LEARN", "STORE",
        "REINVEST", "RECONFIGURE", "SCALE", "ABANDON", "REWORK"
    ]

    GATE_STATES = {
        "CHALLENGE", "PRODUCE", "VERIFY", "DISTRIBUTE",
        "RECONFIGURE", "SCALE"
    }

    VALID_TRANSITIONS: Dict[str, List[str]] = {
        "OBSERVE": ["CAPTURE"],
        "CAPTURE": ["CLASSIFY"],
        "CLASSIFY": ["CONNECT", "RESEARCH"],
        "CONNECT": ["RESEARCH", "SYNTHESIZE"],
        "RESEARCH": ["SYNTHESIZE"],
        "SYNTHESIZE": ["HYPOTHESIZE"],
        "HYPOTHESIZE": ["CHALLENGE"],
        "CHALLENGE": ["PRIORITIZE", "REWORK"],
        "PRIORITIZE": ["DESIGN"],
        "DESIGN": ["SIMULATE"],
        "SIMULATE": ["PRODUCE", "REWORK"],
        "PRODUCE": ["VERIFY"],
        "VERIFY": ["PACKAGE", "REWORK"],
        "PACKAGE": ["DISTRIBUTE"],
        "DISTRIBUTE": ["MEASURE"],
        "MEASURE": ["DIAGNOSE"],
        "DIAGNOSE": ["LEARN"],
        "LEARN": ["STORE"],
        "STORE": ["REINVEST", "RECONFIGURE", "SCALE"],
        "REINVEST": ["RECONFIGURE", "SCALE", "OBSERVE"],
        "RECONFIGURE": ["OBSERVE", "CAPTURE"],
        "SCALE": ["OBSERVE", "MEASURE"],
        "REWORK": ["DESIGN", "SIMULATE", "PRODUCE"],
        "ABANDON": [],
    }

    @classmethod
    def can_transition(cls, current: str, target: str) -> bool:
        return target in cls.VALID_TRANSITIONS.get(current, [])

    @classmethod
    def requires_gate(cls, current: str, target: str) -> bool:
        if current in cls.GATE_STATES:
            return True
        # Additional gate for first-time production and scale
        if target == "DISTRIBUTE" and current == "PACKAGE":
            return True
        return False


class ContextPacket:
    """Structured payload for agent interactions — max 10KB uncompressed."""

    SCHEMA_VERSION = "1.0"
    MAX_SIZE_BYTES = 10240  # 10KB
    REQUIRED_MEMORY_PINS = 1

    def __init__(
        self,
        agent_id: str,
        task_id: str,
        current_state: str,
        target_state: str,
        memory_pins: List[Dict[str, Any]],
        project_context: Dict[str, Any],
        agent_contract: Dict[str, Any],
        human_gate_required: bool = False,
        red_team_pending: bool = False,
    ):
        self.packet_id = str(uuid.uuid4())
        self.version = self.SCHEMA_VERSION
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.agent_context = {
            "agent_id": agent_id,
            "role": self.lookup_role(agent_id),
            "task_id": task_id,
        }
        self.runtime_context = {
            "current_state": current_state,
            "previous_action": self.get_last_action(task_id),
            "errors": self.get_active_errors(task_id),
            "dependencies": [],
            "next_action_target": target_state,
        }
        self.memory_pins = memory_pins
        self.project_context = project_context
        self.agent_contract = agent_contract
        self.state_transition = {
            "current_phase": current_state,
            "target_phase": target_state,
            "conditions_met": self.check_conditions(current_state, target_state),
            "human_gate_required": human_gate_required,
            "red_team_review_pending": red_team_pending,
        }
        self.anti_drift_checks = self.compute_anti_drift(memory_pins, project_context)

    def lookup_role(self, agent_id: str) -> str:
        # Read from agent registry — simplified for v1.0
        registry_path = Path(__file__).parent.parent / "core" / "agent_registry.yaml"
        if registry_path.exists():
            # Basic lookup (full parser would read YAML properly)
            content = registry_path.read_text()
            for line in content.splitlines():
                if agent_id in line and "ROLE" in content:
                    # Return a simplified role from agent ID
                    return agent_id.replace("OMEGA-", "Agent ")
        return agent_id

    def get_last_action(self, task_id: str) -> str:
        # Would read from operational memory
        return "initialized"

    def get_active_errors(self, task_id: str) -> List[str]:
        # Would query failure memory
        return []

    def check_conditions(self, current: str, target: str) -> List[bool]:
        conditions = [
            OmegaState.can_transition(current, target),
            not (OmegaState.requires_gate(current, target) and not self.state_transition["human_gate_required"]),
        ]
        return conditions

    def compute_anti_drift(self, memory_pins: List[Dict], project_context: Dict) -> Dict:
        # Compute pollution score
        banks = set(pin.get("bank_id", "UNKNOWN") for pin in memory_pins)
        score = 0.0
        if len(memory_pins) < self.REQUIRED_MEMORY_PINS:
            score += 0.3
        if not any(pin.get("bank_id") == "FAILURE" for pin in memory_pins):
            score += 0.3  # Critical: must have FAILURE pin
        if len(banks) < 2:
            score += 0.2  # Too narrow
        avg_relevance = sum(pin.get("relevance_score", 0.0) for pin in memory_pins) / max(len(memory_pins), 1)
        if avg_relevance < 0.7:
            score += 0.1

        # Size estimate — compute from raw fields directly, not via to_dict
        packet_components = {
            "packet_id": self.packet_id,
            "timestamp": self.timestamp,
            "agent_context": self.agent_context,
            "runtime_context": self.runtime_context,
            "memory_pins": self.memory_pins,
            "project_context": self.project_context,
            "agent_contract": self.agent_contract,
            "state_transition": self.state_transition,
        }
        packet_json = json.dumps(packet_components, default=str)
        size_bytes = len(packet_json.encode("utf-8"))

        # Thesis alignment
        thesis = project_context.get("thesis_statement", "")
        thesis_check = bool(thesis) and len(thesis) <= 200

        return {
            "max_token_estimate": size_bytes,
            "context_pollution_score": min(score, 1.0),
            "last_memory_sync": datetime.now(timezone.utc).isoformat(),
            "thesis_alignment_check": thesis_check,
            "failure_memory_pin_present": any(pin.get("bank_id") == "FAILURE" for pin in memory_pins),
            "packet_size_bytes": size_bytes,
            "packet_size_valid": size_bytes <= self.MAX_SIZE_BYTES,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "version": self.version,
            "timestamp": self.timestamp,
            "agent_context": self.agent_context,
            "runtime_context": self.runtime_context,
            "memory_pins": self.memory_pins,
            "project_context": self.project_context,
            "agent_contract": self.agent_contract,
            "state_transition": self.state_transition,
            "anti_drift_checks": self.anti_drift_checks,
        }

    def validate(self) -> Tuple[bool, List[str]]:
        errors = []
        if self.anti_drift_checks["packet_size_bytes"] > self.MAX_SIZE_BYTES:
            errors.append(f"Packet exceeds {self.MAX_SIZE_BYTES} bytes: {self.anti_drift_checks['packet_size_bytes']}")
        if self.anti_drift_checks["context_pollution_score"] > 0.3:
            errors.append(f"Pollution score {self.anti_drift_checks['context_pollution_score']} exceeds 0.3")
        if not self.anti_drift_checks["failure_memory_pin_present"]:
            errors.append("FAILURE memory pin is required but missing")
        if not self.anti_drift_checks["thesis_alignment_check"]:
            errors.append("Thesis statement missing or exceeds 200 chars")
        if not OmegaState.can_transition(
            self.state_transition["current_phase"],
            self.state_transition["target_phase"],
        ):
            errors.append(
                f"Invalid state transition: {self.state_transition['current_phase']} → {self.state_transition['target_phase']}"
            )
        return (len(errors) == 0, errors)


class MasterOrchestrator:
    """OMEGA-0 — Routes context packets, manages state machine, activates agents."""

    def __init__(self, registry_path: Optional[str] = None):
        self.name = "OMEGA-0"
        self.code = "MASTER_ORCHESTRATOR"
        self.version = "v1.0.0"
        self.registry_path = registry_path or str(
            Path(__file__).parent.parent.parent / "core" / "agent_registry.yaml"
        )
        self.active_tasks: Dict[str, Any] = {}

    def receive_request(self, user_input: str, role_hint: Optional[str] = None) -> Dict:
        """Entry point: user request → task creation → agent routing."""
        task_id = str(uuid.uuid4())
        # Minimal parsing: treat user input as problem statement for demonstration
        problem_statement = user_input[:200] if len(user_input) > 200 else user_input

        # Create initial context packet
        memory_pins = [
            {
                "bank_id": "FAILURE",
                "entry_id": "init-failure-reference",
                "relevance_score": 0.95,
            },
            {
                "bank_id": "WORLD",
                "entry_id": "world-signal-ref",
                "relevance_score": 0.82,
            },
        ]
        project_context = {
            "project_id": f"project-{task_id[:8]}",
            "thesis_statement": problem_statement,
            "format_constraints": ["documentary", "essay", "short-form"],
            "deadlines": {"concept": "2026-08-29T00:00:00Z"},
            "quality_bar": {"min_omega_score": 0.60, "min_truth_score": 0.80, "max_risk_score": 0.25},
        }
        agent_contract = {
            "role": "Master Orchestrator routing",
            "task": "Route strategic request to appropriate agent crew",
            "available_tools": ["agent_registry.lookup", "context_engine.build_packet", "state_machine.transition"],
            "relevant_knowledge": ["WORLD:init", "STRATEGIC:thesis", "FAILURE:guardrail"],
            "output_contract_ref": "docs/contracts/OUTPUT_CONTRACT_MASTER.md",
            "failure_conditions_ref": "core/agent_registry.yaml",
        }

        packet = ContextPacket(
            agent_id="OMEGA-0",
            task_id=task_id,
            current_state="OBSERVE",
            target_state="CAPTURE",
            memory_pins=memory_pins,
            project_context=project_context,
            agent_contract=agent_contract,
            human_gate_required=False,
        )

        valid, errors = packet.validate()
        if not valid:
            return {
                "status": "ERROR",
                "task_id": task_id,
                "errors": errors,
                "packet_dict": packet.to_dict(),
            }

        # Route to primary agent based on user role or content analysis
        assigned_agent = self.assign_agent(user_input, role_hint)
        packet.agent_context["agent_id"] = assigned_agent
        packet.agent_context["role"] = assigned_agent.replace("OMEGA-", "Agent ")

        # Log activation
        activation_time = 0.0  # Would measure in production
        self.active_tasks[task_id] = {
            "packet": packet,
            "assigned_agent": assigned_agent,
            "status": "ACTIVATED",
            "activation_time_seconds": activation_time,
        }

        return {
            "status": "ACTIVATED",
            "task_id": task_id,
            "assigned_agent": assigned_agent,
            "packet_valid": True,
            "packet_id": packet.packet_id,
            "current_state": packet.state_transition["current_phase"],
            "target_state": packet.state_transition["target_phase"],
            "pollution_score": packet.anti_drift_checks["context_pollution_score"],
            "packet_size_bytes": packet.anti_drift_checks["packet_size_bytes"],
            "failure_pin_present": packet.anti_drift_checks["failure_memory_pin_present"],
            "thesis_check": packet.anti_drift_checks["thesis_alignment_check"],
        }

    def assign_agent(self, user_input: str, role_hint: Optional[str]) -> str:
        # Simple routing rules for v1.0
        if role_hint == "entrepreneur" or "business" in user_input.lower() or "product" in user_input.lower():
            return "OMEGA-P1"
        if role_hint == "creator" or "content" in user_input.lower() or "youtube" in user_input.lower() or "video" in user_input.lower():
            return "OMEGA-C1"
        if role_hint == "filmmaker" or "cinema" in user_input.lower() or "film" in user_input.lower():
            return "OMEGA-F1"
        if role_hint == "ecosystem" or "channel" in user_input.lower() or "system" in user_input.lower():
            return "OMEGA-E1"
        if role_hint == "architect" or "governance" in user_input.lower():
            return "OMEGA-M4"
        if role_hint == "engineer" or "deploy" in user_input.lower():
            return "OMEGA-E2"
        # Default: diagnosis crew for problem statements
        return "OMEGA-D1"

    def execute_agent(self, task_id: str) -> Dict:
        """Simulate agent execution — in production this would invoke agent runtime."""
        task = self.active_tasks.get(task_id)
        if not task:
            return {"status": "ERROR", "message": f"Task {task_id} not found"}

        # Simulate execution time
        time.sleep(0.1)
        packet: ContextPacket = task["packet"]
        agent_id = task["assigned_agent"]

        # In production: agent executes, writes memory, updates state
        # For v1.0: simulate output with contract verification
        output_contract_ref = packet.agent_contract.get("output_contract_ref", "")
        simulated_output = {
            "agent_id": agent_id,
            "task_id": task_id,
            "output_contract_ref": output_contract_ref,
            "execution_time_seconds": 0.3,
            "status": "COMPLETED",
            "memory_updates_planned": [
                {"bank": pin["bank_id"], "entry_ref": pin.get("entry_id", "unknown")}
                for pin in packet.memory_pins
            ],
            "next_target_state": packet.state_transition["target_phase"],
        }

        # Update task state
        task["status"] = "EXECUTED"
        task["simulated_output"] = simulated_output

        return {
            "status": "EXECUTION_COMPLETE",
            "task_id": task_id,
            "agent_executed": agent_id,
            "simulated_output": simulated_output,
            "packet_size_valid": packet.anti_drift_checks["packet_size_valid"],
            "pollution_valid": packet.anti_drift_checks["context_pollution_score"] <= 0.3,
        }

    def get_system_status(self) -> Dict:
        return {
            "orchestrator": self.name,
            "version": self.version,
            "active_tasks": len(self.active_tasks),
            "registry_path": self.registry_path,
            "benchmark_target": "10s activation < 4h content pipeline < 7d product",
            "non_negotiable_rules_active": 12,
        }


if __name__ == "__main__":
    # Basic demonstration / test harness
    orchestrator = MasterOrchestrator()
    status_before = orchestrator.get_system_status()

    # Example user request
    result = orchestrator.receive_request(
        "We need a YouTube series about the future of AI cinema that connects to a digital product for filmmakers.",
        role_hint="filmmaker",
    )
    print(json.dumps(result, indent=2, default=str))

    if result.get("status") == "ACTIVATED" and "task_id" in result:
        execution_result = orchestrator.execute_agent(result["task_id"])
        print(json.dumps(execution_result, indent=2, default=str))
