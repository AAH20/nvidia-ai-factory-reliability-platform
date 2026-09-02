"""Unit tests for Temporal GraphRAG Engine."""

import unittest
from ai_factory_reliability.graphrag import TemporalGraphRAG, GraphNode, GraphEdge


class TestTemporalGraphRAG(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = TemporalGraphRAG()
        # Node 1: Physical GPU node (created at T0, retired at T2)
        self.graph.add_node(GraphNode(
            id="dgx-01",
            layer="physical",
            kind="DGX-H100",
            properties={"region": "us-gov-east", "fips_mode": True},
            valid_from="2026-01-01T00:00:00Z",
            valid_to="2026-06-30T23:59:59Z",
        ))
        # Node 2: NIM Pod (created at T1, ongoing)
        self.graph.add_node(GraphNode(
            id="nim-pod-01",
            layer="workload",
            kind="NIMPod",
            properties={"model": "meta/llama-3.3-70b-instruct", "data_classification": "RESTRICTED"},
            valid_from="2026-03-01T00:00:00Z",
            valid_to="9999-12-31T23:59:59Z",
        ))
        # Edge connecting NIM Pod to DGX-01
        self.graph.add_edge(GraphEdge(
            source="nim-pod-01",
            target="dgx-01",
            relation="SCHEDULED_ON",
            valid_from="2026-03-01T00:00:00Z",
            valid_to="2026-06-30T23:59:59Z",
        ))

    def test_temporal_validity_query(self) -> None:
        # At 2026-04-01 both are valid
        context_active = self.graph.query_temporal_context(query_time="2026-04-01T12:00:00Z", root_id="nim-pod-01")
        self.assertEqual(len(context_active["subgraph_nodes"]), 2)
        self.assertEqual(len(context_active["subgraph_edges"]), 1)

        # At 2026-08-01 DGX-01 is retired and edge is invalid
        context_retired = self.graph.query_temporal_context(query_time="2026-08-01T12:00:00Z", root_id="nim-pod-01")
        self.assertEqual(len(context_retired["subgraph_nodes"]), 1)
        self.assertEqual(len(context_retired["subgraph_edges"]), 0)

    def test_sovereignty_gate(self) -> None:
        # Restricted source to sovereign region passes
        result = self.graph.evaluate_sovereignty_gate("nim-pod-01", "dgx-01")
        self.assertTrue(result["allowed"])

        # Add commercial node without FIPS
        self.graph.add_node(GraphNode(
            id="commercial-node",
            layer="physical",
            kind="CloudVM",
            properties={"region": "eu-west-1", "fips_mode": False},
        ))
        violation = self.graph.evaluate_sovereignty_gate("nim-pod-01", "commercial-node")
        self.assertFalse(violation["allowed"])
        self.assertIn("NIST-800-53-AC-4", violation["control"])


if __name__ == "__main__":
    unittest.main()
