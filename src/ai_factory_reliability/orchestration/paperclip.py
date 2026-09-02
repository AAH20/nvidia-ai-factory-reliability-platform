"""Paperclip Economic and Capacity Budget Governor.

Enforces macro financial boundaries, capacity reservation yield, SLA contract
penalties, and cloud-burst expenditure limits.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class BudgetEvaluation:
    approved: bool
    roi_ratio: float
    expected_revenue_protected_usd: float
    execution_cost_usd: float
    net_economic_value_usd: float
    budget_headroom_usd: float
    reason: str


class PaperclipGovernor:
    """Strategic Financial & Capacity Allocation Authority."""

    def __init__(self, monthly_budget_usd: float = 250_000.0, current_spend_usd: float = 142_000.0) -> None:
        self.monthly_budget_usd = monthly_budget_usd
        self.current_spend_usd = current_spend_usd

    @property
    def headroom_usd(self) -> float:
        return max(0.0, self.monthly_budget_usd - self.current_spend_usd)

    def evaluate_proposal(
        self,
        action_name: str,
        hourly_revenue_at_risk_usd: float,
        outage_duration_hours: float,
        estimated_action_cost_usd: float,
        requires_cloud_burst: bool = False,
    ) -> BudgetEvaluation:
        """Evaluates whether an infrastructure mutation or cloud burst is financially sound."""
        revenue_protected = hourly_revenue_at_risk_usd * outage_duration_hours
        execution_cost = estimated_action_cost_usd
        
        # If cloud burst is required, factor in cross-region egress and premium rate multiplier
        if requires_cloud_burst:
            execution_cost *= 1.35  # 35% premium for on-demand GPU cloud fallback

        net_value = revenue_protected - execution_cost
        roi = revenue_protected / max(1.0, execution_cost)

        # Invariant 1: Action cost must not exceed remaining budget headroom
        if execution_cost > self.headroom_usd:
            return BudgetEvaluation(
                approved=False,
                roi_ratio=roi,
                expected_revenue_protected_usd=revenue_protected,
                execution_cost_usd=execution_cost,
                net_economic_value_usd=net_value,
                budget_headroom_usd=self.headroom_usd,
                reason=f"Execution cost (${execution_cost:,.2f}) exceeds available budget headroom (${self.headroom_usd:,.2f})",
            )

        # Invariant 2: Net economic ROI must be >= 3.0x for automated approval
        if roi < 3.0:
            return BudgetEvaluation(
                approved=False,
                roi_ratio=roi,
                expected_revenue_protected_usd=revenue_protected,
                execution_cost_usd=execution_cost,
                net_economic_value_usd=net_value,
                budget_headroom_usd=self.headroom_usd,
                reason=f"ROI ratio ({roi:.2f}x) is below the minimum mandatory threshold of 3.0x",
            )

        return BudgetEvaluation(
            approved=True,
            roi_ratio=roi,
            expected_revenue_protected_usd=revenue_protected,
            execution_cost_usd=execution_cost,
            net_economic_value_usd=net_value,
            budget_headroom_usd=self.headroom_usd,
            reason="Approved: Value of protected revenue significantly exceeds execution expenditure",
        )
