"""Cryptographic Action Receipts & Tamper-Evident Audit Ledger."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256
from typing import Any


@dataclass
class ActionReceipt:
    receipt_id: str
    incident_id: str
    timestamp: str
    root_cause: str
    action_type: str
    iac_patch_hash: str
    ansible_playbook_hash: str
    compliance_controls_passed: list[str]
    budget_roi_ratio: float
    lease_ttl_minutes: int
    signature_digest: str = field(init=False)

    def __post_init__(self) -> None:
        payload = {
            "receipt_id": self.receipt_id,
            "incident_id": self.incident_id,
            "timestamp": self.timestamp,
            "root_cause": self.root_cause,
            "action_type": self.action_type,
            "iac_patch_hash": self.iac_patch_hash,
            "ansible_playbook_hash": self.ansible_playbook_hash,
            "compliance_controls_passed": self.compliance_controls_passed,
            "budget_roi_ratio": self.budget_roi_ratio,
            "lease_ttl_minutes": self.lease_ttl_minutes,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.signature_digest = sha256(raw).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "incident_id": self.incident_id,
            "timestamp": self.timestamp,
            "root_cause": self.root_cause,
            "action_type": self.action_type,
            "iac_patch_hash": self.iac_patch_hash,
            "ansible_playbook_hash": self.ansible_playbook_hash,
            "compliance_controls_passed": self.compliance_controls_passed,
            "budget_roi_ratio": self.budget_roi_ratio,
            "lease_ttl_minutes": self.lease_ttl_minutes,
            "signature_digest": self.signature_digest,
        }
