"""Temporal GraphRAG causal engine for AI-factory topology, workloads, fabrics, and compliance."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class GraphNode:
    id: str
    layer: str  # physical, fabric, workload, incident, compliance
    kind: str   # GPU, Node, Switch, NIMPod, Change, Policy
    properties: dict[str, Any] = field(default_factory=dict)
    valid_from: str = "1970-01-01T00:00:00Z"
    valid_to: str = "9999-12-31T23:59:59Z"


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str  # CONNECTED_BY_NVLINK, ROUTES_THROUGH, SCHEDULED_ON, MUTATED_BY, CONSTRAINED_BY
    properties: dict[str, Any] = field(default_factory=dict)
    valid_from: str = "1970-01-01T00:00:00Z"
    valid_to: str = "9999-12-31T23:59:59Z"


class TemporalGraphRAG:
    """5-layer temporal causal graph for NVIDIA AI-factory digital twins."""

    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []
        self._adjacency: dict[str, list[GraphEdge]] = {}

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.id] = node
        if node.id not in self._adjacency:
            self._adjacency[node.id] = []

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)
        if edge.source not in self._adjacency:
            self._adjacency[edge.source] = []
        self._adjacency[edge.source].append(edge)

    def is_valid_at(self, valid_from: str, valid_to: str, query_time: str) -> bool:
        """Check if an entity was active at query_time (ISO format comparison)."""
        return valid_from <= query_time <= valid_to

    def query_temporal_context(self, query_time: str, root_id: Optional[str] = None, max_hops: int = 4) -> dict[str, Any]:
        """Extract a sub-graph valid at query_time."""
        active_nodes = {
            nid: n for nid, n in self.nodes.items()
            if self.is_valid_at(n.valid_from, n.valid_to, query_time)
        }
        active_edges = [
            e for e in self.edges
            if self.is_valid_at(e.valid_from, e.valid_to, query_time)
            and e.source in active_nodes and e.target in active_nodes
        ]

        if not root_id or root_id not in active_nodes:
            return {
                "query_time": query_time,
                "node_count": len(active_nodes),
                "edge_count": len(active_edges),
                "nodes": [n.__dict__ for n in active_nodes.values()],
                "edges": [e.__dict__ for e in active_edges],
            }

        # Subgraph traversal from root
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(root_id, 0)]
        subgraph_nodes: set[str] = set()
        subgraph_edges: list[GraphEdge] = []

        adj: dict[str, list[GraphEdge]] = {nid: [] for nid in active_nodes}
        for e in active_edges:
            adj[e.source].append(e)

        while queue:
            curr, depth = queue.pop(0)
            if curr in visited or depth > max_hops:
                continue
            visited.add(curr)
            subgraph_nodes.add(curr)

            for edge in adj.get(curr, []):
                subgraph_edges.append(edge)
                if edge.target not in visited:
                    queue.append((edge.target, depth + 1))

        return {
            "query_time": query_time,
            "root_id": root_id,
            "subgraph_nodes": [active_nodes[nid].__dict__ for nid in subgraph_nodes if nid in active_nodes],
            "subgraph_edges": [e.__dict__ for e in subgraph_edges],
        }

    def trace_causal_path(self, target_service: str, query_time: str) -> list[dict[str, Any]]:
        """Trace dependencies from high-level NIM service down to physical GPUs, switches, and changes."""
        context = self.query_temporal_context(query_time=query_time, root_id=target_service, max_hops=4)
        traces: list[dict[str, Any]] = []

        for edge in context.get("subgraph_edges", []):
            src = self.nodes.get(edge["source"])
            tgt = self.nodes.get(edge["target"])
            if src and tgt:
                traces.append({
                    "from": {"id": src.id, "layer": src.layer, "kind": src.kind},
                    "relation": edge["relation"],
                    "to": {"id": tgt.id, "layer": tgt.layer, "kind": tgt.kind},
                    "properties": edge.get("properties", {}),
                })
        return traces

    def evaluate_sovereignty_gate(self, source_id: str, target_id: str) -> dict[str, Any]:
        """Verify cross-layer boundary compliance (e.g. HIPAA/FedRAMP air-gap)."""
        src = self.nodes.get(source_id)
        tgt = self.nodes.get(target_id)
        if not src or not tgt:
            return {"allowed": False, "reason": "Node not found in topology graph"}

        src_class = src.properties.get("data_classification", "STANDARD")
        tgt_region = tgt.properties.get("region", "unknown")
        tgt_fips = tgt.properties.get("fips_mode", False)

        if src_class == "RESTRICTED":
            if tgt_region not in ("us-gov-east", "us-gov-west", "on-prem-enclave"):
                return {
                    "allowed": False,
                    "reason": f"Sovereignty violation: RESTRICTED data cannot route to {tgt_region}",
                    "control": "NIST-800-53-AC-4",
                }
            if not tgt_fips:
                return {
                    "allowed": False,
                    "reason": "Cryptographic violation: Destination does not enforce FIPS-140-3 mode",
                    "control": "NIST-800-53-SC-8",
                }

        return {"allowed": True, "reason": "Sovereignty boundary verified"}
