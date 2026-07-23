"""Safety contract and counterfactual action gate."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictedOutcome:
    p99_fct_ms: float
    packet_loss_pct: float
    fairness: float
    route_churn_pct: float
    slo_violation_pct: float


@dataclass(frozen=True)
class SafetyLimits:
    max_p99_fct_ms: float = 12.0
    max_packet_loss_pct: float = 0.20
    min_fairness: float = 0.85
    max_route_churn_pct: float = 2.0
    max_slo_violation_pct: float = 8.0


def approve(outcome: PredictedOutcome, limits: SafetyLimits = SafetyLimits()) -> tuple[bool, list[str]]:
    """Approve an action only when every safety invariant is satisfied."""
    reasons: list[str] = []
    if outcome.p99_fct_ms > limits.max_p99_fct_ms:
        reasons.append("predicted P99 flow completion time exceeds limit")
    if outcome.packet_loss_pct > limits.max_packet_loss_pct:
        reasons.append("predicted packet loss exceeds limit")
    if outcome.fairness < limits.min_fairness:
        reasons.append("predicted tenant fairness is below limit")
    if outcome.route_churn_pct > limits.max_route_churn_pct:
        reasons.append("predicted route churn exceeds limit")
    if outcome.slo_violation_pct > limits.max_slo_violation_pct:
        reasons.append("predicted SLO violation rate exceeds limit")
    return not reasons, reasons
