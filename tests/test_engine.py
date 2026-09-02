import copy
import json
from pathlib import Path
import unittest

from ai_factory_reliability.engine import analyze
from ai_factory_reliability.io import load_case


CASE = json.loads((Path(__file__).parents[1] / "examples" / "synthetic-ai-factory-incident.json").read_text())


class EngineTests(unittest.TestCase):
    def test_detects_cross_layer_failures(self):
        result = analyze(*load_case(CASE))
        causes = {finding["cause"] for finding in result["findings"]}
        self.assertTrue({"fabric-degradation", "fabric-congestion", "inference-queue-saturation", "kv-cache-pressure", "nim-replica-unavailable", "stranded-gpu-capacity"}.issubset(causes))
        self.assertEqual(result["release_gate"]["decision"], "eligible-for-simulation")
        self.assertEqual(len(result["receipt_digest"]), 64)

    def test_action_ranking_is_value_based_and_not_execution(self):
        result = analyze(*load_case(CASE))
        values = [action["expected_net_value_usd"] for action in result["ranked_actions"]]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertTrue(all(action["evidence_tier"] == "reference-assumption" for action in result["ranked_actions"]))
        self.assertTrue(all("human-approval" in action["requires"] for action in result["ranked_actions"]))

    def test_unauthorized_action_blocks_simulation(self):
        case = copy.deepcopy(CASE)
        case["snapshot"]["unauthorized_actions"] = 1
        result = analyze(*load_case(case))
        self.assertEqual(result["release_gate"]["decision"], "blocked")

    def test_unverified_snapshot_has_no_verified_revenue(self):
        case = copy.deepcopy(CASE)
        case["snapshot"]["verified"] = False
        result = analyze(*load_case(case))
        self.assertEqual(result["kpis"]["economics"]["verified_revenue_usd"], 0)
        self.assertEqual(result["release_gate"]["decision"], "blocked")


if __name__ == "__main__":
    unittest.main()
