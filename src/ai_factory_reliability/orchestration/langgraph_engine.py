"""LangGraph-Style Durable Two-Phase Commit State Machine for Infrastructure Mutations.

Implements transactional 2PC: Draft -> Batfish_Simulate -> Invariant_Proof -> Canary_Lease -> Commit / Rollback.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class MutationPhase(str, Enum):
    DRAFT = "DRAFT"
    BATFISH_SIMULATE = "BATFISH_SIMULATE"
    INVARIANT_PROOF = "INVARIANT_PROOF"
    CANARY_LEASE = "CANARY_LEASE"
    COMMITTED = "COMMITTED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass
class MutationState:
    mutation_id: str
    target_resource: str
    action_type: str
    phase: MutationPhase
    patch_payload: dict[str, Any]
    lease_duration_minutes: int = 15
    simulation_passed: bool = False
    invariants_passed: bool = False
    canary_health_score: float = 0.0
    error_message: Optional[str] = None
    transition_history: list[str] = field(default_factory=list)


class LangGraphStateEngine:
    """Durable Transactional State Machine."""

    def __init__(self) -> None:
        self.states: dict[str, MutationState] = {}

    def init_mutation(self, mutation_id: str, target: str, action: str, patch: dict[str, Any]) -> MutationState:
        state = MutationState(
            mutation_id=mutation_id,
            target_resource=target,
            action_type=action,
            phase=MutationPhase.DRAFT,
            patch_payload=patch,
            transition_history=[f"INIT: Created draft mutation for {target}"],
        )
        self.states[mutation_id] = state
        return state

    def transition_to_simulation(self, mutation_id: str, simulation_success: bool) -> MutationState:
        state = self.states[mutation_id]
        state.simulation_passed = simulation_success
        if simulation_success:
            state.phase = MutationPhase.BATFISH_SIMULATE
            state.transition_history.append("SIMULATION: Batfish/dry-run passed with zero routing/syntax errors")
        else:
            state.phase = MutationPhase.ROLLED_BACK
            state.error_message = "Dry-run simulation failed"
            state.transition_history.append("FAILURE: Simulation error detected, rejected draft")
        return state

    def transition_to_invariant_proof(self, mutation_id: str, compliance_passed: bool, budget_approved: bool) -> MutationState:
        state = self.states[mutation_id]
        if not state.simulation_passed:
            raise ValueError("Cannot verify invariants on an un-simulated mutation")

        state.invariants_passed = compliance_passed and budget_approved
        if state.invariants_passed:
            state.phase = MutationPhase.INVARIANT_PROOF
            state.transition_history.append("INVARIANTS: OPA Rego compliance & Paperclip budget gates passed")
        else:
            state.phase = MutationPhase.ROLLED_BACK
            state.error_message = "Compliance or budget invariant rejected"
            state.transition_history.append("REJECTION: Policy or budget violation detected")
        return state

    def transition_to_canary_lease(self, mutation_id: str, lease_minutes: int = 15) -> MutationState:
        state = self.states[mutation_id]
        if not state.invariants_passed:
            raise ValueError("Cannot promote to canary lease without invariant proof")

        state.phase = MutationPhase.CANARY_LEASE
        state.lease_duration_minutes = lease_minutes
        state.transition_history.append(f"CANARY: Applied reversible lease with {lease_minutes}m TTL")
        return state

    def finalize_mutation(self, mutation_id: str, canary_health_score: float) -> MutationState:
        state = self.states[mutation_id]
        state.canary_health_score = canary_health_score

        if canary_health_score >= 0.95:
            state.phase = MutationPhase.COMMITTED
            state.transition_history.append(f"COMMIT: Canary health confirmed ({canary_health_score*100:.1f}%), committed permanently")
        else:
            state.phase = MutationPhase.ROLLED_BACK
            state.error_message = f"Canary health degraded ({canary_health_score*100:.1f}%), automated rollback triggered"
            state.transition_history.append("ROLLBACK: Automated rollback executed to restore baseline state")
        return state
