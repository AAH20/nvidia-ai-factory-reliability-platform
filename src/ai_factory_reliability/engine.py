from dataclasses import asdict
from hashlib import sha256
import json

from .diagnosis import diagnose
from .kpis import calculate
from .models import FactorySnapshot, FabricLink, WorkloadSLO
from .prescription import rank_actions
from .topology import FactoryTopology


def analyze(links: list[FabricLink], roots: tuple[str, ...], snapshot: FactorySnapshot, slo: WorkloadSLO) -> dict:
    topology = FactoryTopology(links).analyze(roots)
    kpis = calculate(snapshot, slo)
    findings = diagnose(kpis, topology, slo)
    actions = rank_actions(findings)
    checks = {
        "verified_observations": snapshot.verified,
        "zero_unauthorized_actions": snapshot.unauthorized_actions == 0,
        "evaluations_complete": kpis["agent"]["evaluation_pass_rate"] == 1,
        "policy_complete": kpis["agent"]["policy_pass_rate"] == 1,
        "dependency_coverage": kpis["agent"]["dependency_coverage"] >= .95,
    }
    payload = {
        "slo": asdict(slo),
        "topology": topology,
        "kpis": kpis,
        "findings": findings,
        "ranked_actions": actions,
        "release_gate": {"decision": "eligible-for-simulation" if all(checks.values()) else "blocked", "checks": checks},
        "evidence_tiers": {"engine": "implemented", "scenario": "simulated", "integrations": "contract", "action_economics": "reference-assumption"},
    }
    payload["receipt_digest"] = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return payload
