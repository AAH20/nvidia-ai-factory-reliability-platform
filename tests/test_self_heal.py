"""Integration test for Autonomous Self-Healing Pipeline."""

import json
from pathlib import Path
import unittest

from ai_factory_reliability.self_heal import run_self_healing_pipeline


FIXTURE_PATH = Path(__file__).parents[1] / "examples" / "roce-pfc-deadlock-llama3.json"


class TestSelfHealingIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.incident_data = json.loads(FIXTURE_PATH.read_text())

    def test_complete_self_healing_pipeline_execution(self) -> None:
        result = run_self_healing_pipeline(self.incident_data)

        # 1. Pipeline status and diagnosis
        self.assertEqual(result["status"], "SELF_HEALED_AND_VERIFIED")
        self.assertIn("RoCEv2 Fabric Congestion", result["root_cause_analysis"])

        # 2. Crew consensus
        self.assertEqual(len(result["crew_debate"]), 4)
        roles = {opinion["agent_role"] for opinion in result["crew_debate"]}
        self.assertEqual(roles, {
            "NIM Performance Specialist",
            "Network Fabric Specialist",
            "Compliance Auditor",
            "IaC Synthesizer",
        })

        # 3. Financial Governor (Paperclip)
        fin = result["financial_governance"]
        self.assertTrue(fin["approved"])
        self.assertGreater(fin["expected_revenue_protected_usd"], fin["execution_cost_usd"])
        self.assertGreaterEqual(fin["roi_ratio"], 3.0)

        # 4. Compliance as Code
        comp = result["compliance_audit"]
        self.assertTrue(comp["passed"])
        self.assertEqual(len(comp["violations"]), 0)

        # 5. Synthesized Artifacts
        tofu = result["synthesized_iac_patch"]
        self.assertIn("resource \"kubernetes_deployment\"", tofu["hcl_content"])
        self.assertIn("replicas = 8", tofu["hcl_content"])

        ansible = result["synthesized_network_playbook"]
        self.assertIn("ecn.wred_enable = true", ansible["playbook_yaml"])
        self.assertIn("pfc.lossless_priorities = 3", ansible["playbook_yaml"])

        # 6. Cryptographic Action Receipt
        receipt = result["cryptographic_action_receipt"]
        self.assertEqual(len(receipt["signature_digest"]), 64)
        self.assertEqual(receipt["incident_id"], "INC-2026-NVIDIA-ROCE-089")
        self.assertEqual(receipt["lease_ttl_minutes"], 15)


if __name__ == "__main__":
    unittest.main()
