from .models import FactorySnapshot, FabricLink, WorkloadSLO


def load_case(document: dict):
    links = [FabricLink(**item) for item in document["fabric_links"]]
    snapshot = dict(document["snapshot"])
    snapshot["tags"] = tuple(snapshot.get("tags", []))
    return links, tuple(document["roots"]), FactorySnapshot(**snapshot), WorkloadSLO(**document["slo"])
