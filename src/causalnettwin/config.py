"""Configuration objects for the CausalNetTwin reproducible simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Scenario:
    """Parameters describing a reproducible fabric stress scenario."""

    name: str
    topology: str
    severity: float
    burstiness: float
    oversubscription: float
    failure_probability: float
    storage_pressure: float
    ai_collective_intensity: float
    slo_ms: float


@dataclass(frozen=True)
class MethodProfile:
    """Behavioral profile used by each remediation policy."""

    name: str
    trigger_threshold: float
    diagnostic_accuracy: float
    action_efficacy: float
    wrong_action_penalty: float
    safety_rejection: float
    rollback_detection: float
    churn_factor: float
    telemetry_overhead_pct: float
    inference_latency_ms: float


SCENARIOS: Tuple[Scenario, ...] = (
    Scenario("leaf_spine_mixed", "leaf-spine", 1.00, 0.35, 1.15, 0.00, 0.45, 0.50, 8.0),
    Scenario("fat_tree_allreduce", "fat-tree", 1.12, 0.55, 1.05, 0.00, 0.25, 0.92, 8.5),
    Scenario("oversubscribed_multi_tenant", "leaf-spine-4to1", 1.35, 0.62, 1.45, 0.00, 0.55, 0.66, 9.0),
    Scenario("link_failure", "leaf-spine", 1.42, 0.48, 1.25, 0.08, 0.42, 0.58, 9.5),
    Scenario("elephant_flow_arrival", "fat-tree", 1.26, 0.75, 1.20, 0.00, 0.38, 0.64, 9.0),
    Scenario("backup_ai_collision", "leaf-spine-4to1", 1.58, 0.70, 1.50, 0.00, 0.95, 0.95, 10.0),
)

METHODS: Tuple[MethodProfile, ...] = (
    MethodProfile("ECMP", 2.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.35, 0.18),
    MethodProfile("Static-TE", 0.96, 0.82, 0.16, 0.18, 0.00, 0.00, 0.05, 0.55, 0.45),
    MethodProfile("Correlation-ML", 0.82, 0.72, 0.31, 0.49, 0.00, 0.00, 0.20, 1.45, 2.90),
    MethodProfile("DRL", 0.80, 0.79, 0.39, 0.58, 0.00, 0.00, 0.25, 1.75, 4.80),
    MethodProfile("Twin-No-Causal", 0.78, 0.85, 0.45, 0.45, 0.05, 0.28, 0.16, 2.10, 5.70),
    MethodProfile("CausalNetTwin", 0.76, 0.94, 0.58, 0.38, 0.90, 0.94, 0.08, 2.65, 7.20),
)

METHOD_MAP: Dict[str, MethodProfile] = {m.name: m for m in METHODS}
SCENARIO_MAP: Dict[str, Scenario] = {s.name: s for s in SCENARIOS}
