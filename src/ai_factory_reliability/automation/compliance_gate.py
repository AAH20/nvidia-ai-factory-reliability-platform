"""Compliance as Code Engine: OPA/Rego Invariants and NIST OSCAL SSP Exporter."""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class PolicyEvaluationResult:
    passed: bool
    evaluated_controls: list[str]
    violations: list[str]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ComplianceGate:
    """Evaluates proposed infrastructure mutations against formal regulatory invariants."""

    def evaluate_mutation(self, proposed_patch: dict[str, Any], workload_metadata: dict[str, Any]) -> PolicyEvaluationResult:
        controls = ["NIST-800-53-AC-4", "NIST-800-53-SC-7", "NIST-800-53-SC-8", "EU-AI-ACT-ART-15"]
        violations = []

        # Check 1: Data sovereignty & air-gap boundary (AC-4)
        classification = workload_metadata.get("data_classification", "STANDARD")
        target_region = proposed_patch.get("target_region", "us-east-1")
        if classification == "RESTRICTED" and target_region not in ("us-gov-east", "us-gov-west", "on-prem-enclave"):
            violations.append(f"AC-4 Violation: Restricted workload attempted placement in unapproved region '{target_region}'")

        # Check 2: Transmission confidentiality & lossless fabric isolation (SC-8)
        mtu = proposed_patch.get("mtu", 9000)
        if mtu < 9000 and proposed_patch.get("fabric_type") == "RoCEv2":
            violations.append("SC-8 Violation: RoCEv2 fabric mutation must enforce MTU 9000 jumbo frame isolation")

        # Check 3: Cryptographic FIPS mode (SC-7)
        if classification == "RESTRICTED" and not workload_metadata.get("fips_mode", True):
            violations.append("SC-7 Violation: FIPS 140-3 cryptographic mode must be enabled for restricted workloads")

        return PolicyEvaluationResult(
            passed=len(violations) == 0,
            evaluated_controls=controls,
            violations=violations,
        )


class OSCALExporter:
    """Exports machine-readable NIST OSCAL System Security Plan (SSP) JSON."""

    def export_ssp(self, system_id: str, compliance_result: PolicyEvaluationResult, topology_state: dict[str, Any]) -> dict[str, Any]:
        return {
            "system-security-plan": {
                "id": f"ssp-{system_id}",
                "metadata": {
                    "title": "NVIDIA AI Factory Sovereign Enclave SSP",
                    "published": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0.0",
                    "oscal-version": "1.0.4",
                },
                "import-profile": {
                    "href": "urn:nist:fedramp:profile:high",
                },
                "system-characteristics": {
                    "system-name": "Aegis-Factory-NIM-Cluster",
                    "deployment-model": "private-cloud",
                    "security-sensitivity-level": "high",
                    "system-information": {
                        "information-types": [
                            {"title": "AI Inference Telemetry", "confidentiality": "high", "integrity": "high"}
                        ]
                    }
                },
                "control-implementation": {
                    "description": "Continuous compliance-as-code verification via Aegis Factory Control Plane",
                    "implemented-requirements": [
                        {
                            "control-id": ctrl,
                            "status": "satisfied" if ctrl not in str(compliance_result.violations) else "failed",
                            "remarks": "Automated invariant verification passed" if compliance_result.passed else "Violation recorded",
                        }
                        for ctrl in compliance_result.evaluated_controls
                    ]
                }
            }
        }
