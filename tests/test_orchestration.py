"""Unit tests for Multi-Tier Orchestration (Paperclip, OpenClaw, LangGraph, Crew)."""

import unittest
from ai_factory_reliability.orchestration.paperclip import PaperclipGovernor
from ai_factory_reliability.orchestration.openclaw import OpenClawGateway, OperationalSkill, EventTrigger
from ai_factory_reliability.orchestration.langgraph_engine import LangGraphStateEngine, MutationPhase
from ai_factory_reliability.orchestration.crew import SpecialistCrew


class TestOrchestration(unittest.TestCase):
    def test_paperclip_governor_enforces_roi_and_budget(self) -> None:
        governor = PaperclipGovernor(monthly_budget_usd=100_000.0, current_spend_usd=90_000.0)
        # Headroom is 10,000

        # Scenario 1: Cost exceeds headroom
        eval1 = governor.evaluate_proposal(
            action_name="expensive_cluster_expansion",
            hourly_revenue_at_risk_usd=50_000.0,
            outage_duration_hours=1.0,
            estimated_action_cost_usd=15_000.0,
        )
        self.assertFalse(eval1.approved)
        self.assertIn("exceeds available budget headroom", eval1.reason)

        # Scenario 2: ROI below 3.0x threshold
        eval2 = governor.evaluate_proposal(
            action_name="marginal_optimization",
            hourly_revenue_at_risk_usd=2_000.0,
            outage_duration_hours=1.0,
            estimated_action_cost_usd=1_000.0,
        )
        self.assertFalse(eval2.approved)
        self.assertIn("minimum mandatory threshold of 3.0x", eval2.reason)

        # Scenario 3: High ROI, within budget
        eval3 = governor.evaluate_proposal(
            action_name="pfc_tuning",
            hourly_revenue_at_risk_usd=10_000.0,
            outage_duration_hours=2.0,
            estimated_action_cost_usd=100.0,
        )
        self.assertTrue(eval3.approved)
        self.assertGreaterEqual(eval3.roi_ratio, 3.0)

    def test_openclaw_gateway_triggers_and_skill_mesh(self) -> None:
        gateway = OpenClawGateway()
        called = False

        def mock_heal():
            nonlocal called
            called = True
            return "SUCCESS"

        gateway.register_skill(OperationalSkill(
            name="heal_roce_fabric_pfc",
            version="1.0.0",
            description="RoCEv2 PFC Healing",
            required_role="network_engineer",
            handler=mock_heal,
        ))

        # Ingest alert below threshold
        low_event = gateway.ingest_event(EventTrigger(
            event_id="EVT-01",
            source="dcgm",
            severity="INFO",
            metric_name="roce_pause_duration",
            observed_value=5.0,
            threshold=50.0,
        ))
        self.assertEqual(low_event["status"], "NORMAL")
        self.assertEqual(len(low_event["matched_skills"]), 0)

        # Ingest breach alert
        breach_event = gateway.ingest_event(EventTrigger(
            event_id="EVT-02",
            source="dcgm",
            severity="CRITICAL",
            metric_name="roce_pause_duration",
            observed_value=120.0,
            threshold=50.0,
        ))
        self.assertEqual(breach_event["status"], "ACTION_REQUIRED")
        self.assertIn("heal_roce_fabric_pfc", breach_event["matched_skills"])

        # Execute registered skill
        res = gateway.execute_skill("heal_roce_fabric_pfc")
        self.assertTrue(called)
        self.assertEqual(res, "SUCCESS")

    def test_langgraph_2pc_state_machine_happy_path(self) -> None:
        engine = LangGraphStateEngine()
        mut = engine.init_mutation("MUT-01", "nim-cluster", "SCALE", {"replicas": 8})
        self.assertEqual(mut.phase, MutationPhase.DRAFT)

        engine.transition_to_simulation("MUT-01", simulation_success=True)
        self.assertEqual(mut.phase, MutationPhase.BATFISH_SIMULATE)

        engine.transition_to_invariant_proof("MUT-01", compliance_passed=True, budget_approved=True)
        self.assertEqual(mut.phase, MutationPhase.INVARIANT_PROOF)

        engine.transition_to_canary_lease("MUT-01", lease_minutes=15)
        self.assertEqual(mut.phase, MutationPhase.CANARY_LEASE)

        engine.finalize_mutation("MUT-01", canary_health_score=0.99)
        self.assertEqual(mut.phase, MutationPhase.COMMITTED)

    def test_langgraph_2pc_state_machine_canary_rollback(self) -> None:
        engine = LangGraphStateEngine()
        mut = engine.init_mutation("MUT-02", "leaf-switch", "QOS_UPDATE", {})
        engine.transition_to_simulation("MUT-02", simulation_success=True)
        engine.transition_to_invariant_proof("MUT-02", compliance_passed=True, budget_approved=True)
        engine.transition_to_canary_lease("MUT-02", lease_minutes=15)

        # Canary health drops to 75%
        engine.finalize_mutation("MUT-02", canary_health_score=0.75)
        self.assertEqual(mut.phase, MutationPhase.ROLLED_BACK)
        self.assertIn("Automated rollback", mut.transition_history[-1])


if __name__ == "__main__":
    unittest.main()
