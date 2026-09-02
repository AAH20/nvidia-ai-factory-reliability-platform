from collections import defaultdict, deque

from .models import FabricLink


class FactoryTopology:
    def __init__(self, links: list[FabricLink]):
        self.links = links

    def analyze(self, roots: tuple[str, ...], max_hops: int = 4) -> dict:
        graph: dict[str, list[tuple[str, FabricLink]]] = defaultdict(list)
        for link in self.links:
            graph[link.source].append((link.target, link))
            graph[link.target].append((link.source, link))
        queue = deque((root, 0) for root in roots)
        visited = set()
        traversed = []
        while queue:
            node, depth = queue.popleft()
            if node in visited or depth > max_hops:
                continue
            visited.add(node)
            for neighbor, link in sorted(graph[node], key=lambda item: item[0]):
                traversed.append({
                    "source": node,
                    "target": neighbor,
                    "kind": link.kind,
                    "utilization": link.utilization,
                    "packet_loss_rate": link.packet_loss_rate,
                    "healthy": link.healthy,
                    "depth": depth + 1,
                })
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        unhealthy = [link for link in traversed if not link["healthy"]]
        congested = [link for link in traversed if link["utilization"] >= .85]
        lossy = [link for link in traversed if link["packet_loss_rate"] > 0]
        return {
            "roots": list(roots),
            "resources": sorted(visited),
            "links": traversed,
            "unhealthy_links": unhealthy,
            "congested_links": congested,
            "lossy_links": lossy,
        }
