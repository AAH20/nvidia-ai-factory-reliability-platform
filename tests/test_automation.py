"""Unit tests for Automation (OpenTofu, Ansible, ComplianceGate, OSCAL)."""

import unittest
from ai_factory_reliability.automation.opentofu_generator import OpenTofuSynthesizer
from ai_factory_reliability.automation.ansible_generator import AnsibleNetworkSynthesizer
from ai_factory_reliability.automation.compliance_gate import ComplianceGate, OSCALExporter, PolicyEvaluationResult


class TestAutomation(unittest.TestCase):
    def test_opentofu_synthesizer_generates_valid_hcl(self) -> None:
        tofu = OpenTofuSynthesizer()
        patch = tofu.generate_nim_scaling_patch(
            service_name="meta-llama3-70b",
            current_replicas=4,
            target_replicas=8,
            gpu_type="nvidia.com/gpu",
            gpus_per_replica=8,
        )
        self.assertIn("resource \"kubernetes_deployment\" \"meta-llama3-70b\"", patch.hcl_content)
        self.assertIn("replicas = 8", patch.hcl_content)
        self.assertIn("\"nvidia.com/gpu\" = \"8\"", patch.hcl_content)
        self.assertIn("replicas = 4", patch.rollback_hcl)

    def test_ansible_network_synthesizer_generates_roce_qos(self) -> None:
        ansible = AnsibleNetworkSynthesizer()
        playbook = ansible.generate_roce_qos_playbook(
            switch_group="leaf_switches",
            pfc_cos_priority=3,
            ecn_min_threshold_kb=150,
            ecn_max_threshold_kb=1500,
            mtu=9000,
        )
        self.assertIn("hosts: leaf_switches", playbook.playbook_yaml)
        self.assertIn("pfc.lossless_priorities = 3", playbook.playbook_yaml)
        self.assertIn("mtu 9000", playbook.playbook_yaml)
        self.assertIn("service:\n        name: switchd", playbook.playbook_yaml)

    def test_compliance_gate_enforces_nist_and_sovereignty(self) -> None:
        gate = ComplianceGate()

        # Passing evaluation
        res_pass = gate.evaluate_mutation(
            proposed_patch={"target_region": "us-gov-east", "mtu": 9000, "fabric_type": "RoCEv2"},
            workload_metadata={"data_classification": "RESTRICTED", "fips_mode": True},
        )
        self.assertTrue(res_pass.passed)
        self.assertEqual(len(res_pass.violations), 0)

        # Violation: restricted data in commercial region
        res_fail = gate.evaluate_mutation(
            proposed_patch={"target_region": "us-east-1", "mtu": 9000, "fabric_type": "RoCEv2"},
            workload_metadata={"data_classification": "RESTRICTED", "fips_mode": True},
        )
        self.assertFalse(res_fail.passed)
        self.assertTrue(any("AC-4" in v for v in res_fail.violations))

    def test_oscal_ssp_exporter_structure(self) -> None:
        exporter = OSCALExporter()
        mock_eval = PolicyEvaluationResult(
            passed=True,
            evaluated_controls=["NIST-800-53-AC-4", "NIST-800-53-SC-7"],
            violations=[],
        )
        ssp = exporter.export_ssp("cluster-01", mock_eval, {})
        self.assertIn("system-security-plan", ssp)
        plan = ssp["system-security-plan"]
        self.assertEqual(plan["metadata"]["oscal-version"], "1.0.4")
        self.assertEqual(len(plan["control-implementation"]["implemented-requirements"]), 2)


if __name__ == "__main__":
    unittest.main()
