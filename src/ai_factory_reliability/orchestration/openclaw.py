"""OpenClaw-Compatible Gateway & Reusable Skill Mesh.

Provides the persistent operational daemon, event-driven Prometheus/DCGM trigger
listeners, and hot-reloadable skill execution mesh.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Any


@dataclass
class OperationalSkill:
    name: str
    version: str
    description: str
    required_role: str
    handler: Callable[..., Any]
    enabled: bool = True


@dataclass
class EventTrigger:
    event_id: str
    source: str  # prometheus, dcgm, kubernetes, nim
    severity: str
    metric_name: str
    observed_value: float
    threshold: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OpenClawGateway:
    """Persistent Operator Runtime and Skill Mesh."""

    def __init__(self) -> None:
        self.skills: dict[str, OperationalSkill] = {}
        self.event_log: list[EventTrigger] = []

    def register_skill(self, skill: OperationalSkill) -> None:
        self.skills[skill.name] = skill

    def ingest_event(self, trigger: EventTrigger) -> dict[str, Any]:
        """Ingests an infrastructure or telemetry event and matches against operational skills."""
        self.event_log.append(trigger)
        is_breach = trigger.observed_value >= trigger.threshold

        matched_skills = []
        if is_breach:
            if "pfc" in trigger.metric_name.lower() or "roce" in trigger.metric_name.lower():
                matched_skills.append("heal_roce_fabric_pfc")
            if "ttft" in trigger.metric_name.lower() or "latency" in trigger.metric_name.lower():
                matched_skills.append("rebalance_nim_replicas")
            if "kv_cache" in trigger.metric_name.lower():
                matched_skills.append("compact_kv_cache_pool")

        return {
            "trigger_id": trigger.event_id,
            "status": "ACTION_REQUIRED" if is_breach else "NORMAL",
            "matched_skills": [s for s in matched_skills if s in self.skills],
            "severity": trigger.severity,
            "timestamp": trigger.timestamp,
        }

    def execute_skill(self, skill_name: str, **kwargs: Any) -> Any:
        if skill_name not in self.skills:
            raise KeyError(f"Skill '{skill_name}' is not registered in OpenClaw gateway")
        skill = self.skills[skill_name]
        if not skill.enabled:
            raise RuntimeError(f"Skill '{skill_name}' is disabled")
        return skill.handler(**kwargs)
