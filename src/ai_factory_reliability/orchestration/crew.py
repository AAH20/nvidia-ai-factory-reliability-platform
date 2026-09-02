"""CrewAI-Style Specialist Collaboration and Bounded Debate.

Contains four specialist agents:
1. NIM Performance Specialist (Inference & KV-cache)
2. Network Fabric Specialist (RoCEv2, PFC, ECN, InfiniBand)
3. Compliance Auditor (Sovereignty, NIST 800-53, FIPS)
4. IaC Synthesizer (OpenTofu HCL & Ansible YAML)
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class SpecialistOpinion:
    agent_role: str
    assessment: str
    proposed_remediation: str
    confidence: float
    risk_level: str


@dataclass
class CrewConsensus:
    agreed_root_cause: str
    primary_remediation: str
    confidence_score: float
    specialist_opinions: list[SpecialistOpinion]
    execution_risk: str


class SpecialistCrew:
    """Orchestrates specialist agent cross-examination within bounded stages."""

    def debate_incident(self, incident_telemetry: dict[str, Any], topology_context: dict[str, Any]) -> CrewConsensus:
        metrics = incident_telemetry.get("metrics", {})
        
        # 1. NIM Performance Specialist
        ttft = metrics.get("p95_ttft_ms", 450)
        kv_fraction = metrics.get("kv_cache_fraction", 0.6)
        nim_assessment = "Healthy"
        nim_action = "Maintain current replica count"
        if ttft > 1000 or kv_fraction > 0.85:
            nim_assessment = f"CRITICAL: TTFT spike ({ttft}ms) and KV-cache pressure ({kv_fraction*100:.1f}%)"
            nim_action = "Expand batch worker pools and re-partition MIG slices"

        nim_op = SpecialistOpinion(
            agent_role="NIM Performance Specialist",
            assessment=nim_assessment,
            proposed_remediation=nim_action,
            confidence=0.92,
            risk_level="MEDIUM",
        )

        # 2. Network Fabric Specialist
        pfc_pauses = metrics.get("pfc_pause_duration_ms", 0)
        loss_rate = metrics.get("packet_loss_rate", 0.0)
        net_assessment = "Fabric links nominal"
        net_action = "No fabric change required"
        if pfc_pauses > 50 or loss_rate > 0.001:
            net_assessment = f"ALERT: RoCEv2 PFC pause storm detected ({pfc_pauses}ms pause duration, loss={loss_rate*100:.2f}%)"
            net_action = "Adjust switch ECN WRED thresholds and rebalance lossless queue buffer headroom via Ansible"

        net_op = SpecialistOpinion(
            agent_role="Network Fabric Specialist",
            assessment=net_assessment,
            proposed_remediation=net_action,
            confidence=0.96,
            risk_level="LOW",
        )

        # 3. Compliance Auditor
        data_class = incident_telemetry.get("data_classification", "STANDARD")
        target_region = incident_telemetry.get("target_region", "us-east-1")
        fips = incident_telemetry.get("fips_mode", True)
        comp_assessment = "Sovereignty boundary intact"
        comp_action = "Approve remediation within existing enclave"
        if data_class == "RESTRICTED" and target_region not in ("us-gov-east", "us-gov-west", "on-prem-enclave"):
            comp_assessment = f"VIOLATION: RESTRICTED workload cannot route to commercial region {target_region}"
            comp_action = "Veto cross-region burst; enforce local node drain only"

        comp_op = SpecialistOpinion(
            agent_role="Compliance Auditor",
            assessment=comp_assessment,
            proposed_remediation=comp_action,
            confidence=0.99,
            risk_level="HIGH" if "VIOLATION" in comp_assessment else "LOW",
        )

        # 4. IaC Synthesizer
        iac_op = SpecialistOpinion(
            agent_role="IaC Synthesizer",
            assessment="Ready to compile declarative OpenTofu HCL and Ansible YAML patch",
            proposed_remediation="Generate dual-target configuration patch with rollback recipe",
            confidence=0.95,
            risk_level="LOW",
        )

        opinions = [nim_op, net_op, comp_op, iac_op]

        # Formulate consensus
        if "ALERT" in net_assessment:
            consensus_cause = "RoCEv2 Fabric Congestion triggering Priority Flow Control (PFC) pause storm and downstream NIM latency"
            consensus_remediation = "Apply Ansible switch QoS tuning (ECN WRED thresholds) and OpenTofu GPU affinity rebalancing"
        elif "CRITICAL" in nim_assessment:
            consensus_cause = "Inference KV-Cache saturation on overloaded GPU nodes"
            consensus_remediation = "Scale NIM pod replicas and repartition MIG instances via OpenTofu"
        else:
            consensus_cause = "Nominal operating state"
            consensus_remediation = "No intervention needed"

        return CrewConsensus(
            agreed_root_cause=consensus_cause,
            primary_remediation=consensus_remediation,
            confidence_score=0.95,
            specialist_opinions=opinions,
            execution_risk="LOW",
        )
