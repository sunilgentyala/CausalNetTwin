"""Deployment verification and rollback decision logic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationWindow:
    predicted_p99_ms: float
    observed_p99_ms: float
    predicted_loss_pct: float
    observed_loss_pct: float
    deviation_tolerance: float = 0.20


def should_rollback(window: VerificationWindow) -> bool:
    """Return True when observed outcomes deviate materially and worsen safety."""
    p99_gap = (window.observed_p99_ms - window.predicted_p99_ms) / max(window.predicted_p99_ms, 1e-9)
    loss_gap = (window.observed_loss_pct - window.predicted_loss_pct) / max(window.predicted_loss_pct, 0.01)
    return (p99_gap > window.deviation_tolerance and window.observed_p99_ms > window.predicted_p99_ms) or (
        loss_gap > window.deviation_tolerance and window.observed_loss_pct > window.predicted_loss_pct
    )
