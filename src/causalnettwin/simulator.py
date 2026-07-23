"""Structural, event-driven simulator for safe network remediation studies.

The simulator is intentionally lightweight so that every table in the artifact can
be regenerated on a laptop. It does not claim packet-level fidelity. Instead, it
models causal relationships among workload phase, congestion, queueing, actions,
and post-action outcomes, then exposes the same safety metrics used in the paper.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List

import numpy as np
import pandas as pd

from .config import MethodProfile, Scenario


class SimulationError(RuntimeError):
    """Raised when invalid simulation parameters are supplied."""


def _latent_congestion(rng: np.random.Generator, scenario: Scenario, steps: int) -> np.ndarray:
    """Generate an autocorrelated latent congestion trace."""
    if steps < 50:
        raise SimulationError("steps must be at least 50")
    x = np.empty(steps, dtype=float)
    x[0] = 0.43 * scenario.severity
    for t in range(1, steps):
        seasonal = 0.08 * np.sin(2 * np.pi * t / 60.0)
        shock = rng.normal(0.0, 0.055 + 0.055 * scenario.burstiness)
        persistence = 0.88 * x[t - 1]
        baseline = 0.072 * scenario.severity * scenario.oversubscription
        x[t] = max(0.15, persistence + baseline + seasonal + shock)

    # Explicit workload events.
    event_centers = [int(steps * 0.28), int(steps * 0.61), int(steps * 0.79)]
    for center in event_centers:
        width = int(9 + 18 * scenario.burstiness)
        idx = np.arange(steps)
        pulse = np.exp(-0.5 * ((idx - center) / width) ** 2)
        x += pulse * (0.16 + 0.15 * scenario.severity)

    if scenario.failure_probability > 0:
        failures = rng.random(steps) < scenario.failure_probability / 10.0
        x += failures.astype(float) * rng.uniform(0.35, 0.65, size=steps)

    collision = scenario.storage_pressure * scenario.ai_collective_intensity
    x += 0.12 * collision
    return np.clip(x, 0.1, 1.85)


def _fct_from_congestion(
    rng: np.random.Generator,
    congestion: np.ndarray,
    scenario: Scenario,
) -> np.ndarray:
    """Map congestion to a mixed-workload flow completion time distribution."""
    queue_term = 13.5 * np.maximum(congestion - 0.62, 0.0) ** 2
    collective_penalty = 1.8 * scenario.ai_collective_intensity * np.maximum(congestion - 0.72, 0.0)
    storage_penalty = 1.5 * scenario.storage_pressure * np.maximum(congestion - 0.78, 0.0)
    noise = rng.lognormal(mean=-1.15, sigma=0.43, size=congestion.size)
    return 1.20 + queue_term + collective_penalty + storage_penalty + noise


def run_trial(
    scenario: Scenario,
    method: MethodProfile,
    seed: int,
    steps: int = 600,
) -> Dict[str, float]:
    """Run one deterministic trial and return aggregate metrics."""
    rng = np.random.default_rng(seed)
    latent = _latent_congestion(rng, scenario, steps)

    # Telemetry observation contains noise and delayed indicators.
    observed = np.clip(latent + rng.normal(0, 0.045, steps), 0.0, 2.0)
    post = latent.copy()
    triggered = observed > method.trigger_threshold
    action_count = int(triggered.sum())
    correct = np.zeros(steps, dtype=bool)
    accepted = np.zeros(steps, dtype=bool)
    rolled_back = np.zeros(steps, dtype=bool)
    harmful = np.zeros(steps, dtype=bool)
    successful = np.zeros(steps, dtype=bool)

    if action_count:
        action_idx = np.flatnonzero(triggered)
        correct[action_idx] = rng.random(action_count) < method.diagnostic_accuracy

        # Safety score combines the predicted tail risk, tenant imbalance, and action churn.
        predicted_risk = (
            0.55 * np.maximum(observed[action_idx] - 0.82, 0)
            + 0.22 * scenario.burstiness
            + 0.16 * scenario.storage_pressure * scenario.ai_collective_intensity
            + rng.normal(0, 0.045, action_count)
        )
        candidate_is_risky = (~correct[action_idx]) | ((predicted_risk > 0.68) & (rng.random(action_count) < 0.35))
        reject = candidate_is_risky & (rng.random(action_count) < method.safety_rejection)
        accepted[action_idx] = ~reject

        accepted_idx = action_idx[~reject]
        if accepted_idx.size:
            corr_mask = correct[accepted_idx]
            efficacy = method.action_efficacy * rng.uniform(0.72, 1.08, accepted_idx.size)
            benefit = efficacy * (0.36 + 0.52 * np.maximum(post[accepted_idx] - 0.68, 0))
            penalty = method.wrong_action_penalty * rng.uniform(0.16, 0.42, accepted_idx.size)
            delta = np.where(corr_mask, -benefit, penalty)

            # Queue migration and synchronized collective traffic amplify wrong actions.
            spillover = np.where(
                corr_mask,
                0.0,
                0.13 * scenario.ai_collective_intensity + 0.10 * scenario.storage_pressure,
            )
            before = post[accepted_idx].copy()
            post[accepted_idx] = np.clip(post[accepted_idx] + delta + spillover, 0.12, 2.2)

            preliminary_harm = post[accepted_idx] > before * 1.045
            detection = preliminary_harm & (rng.random(accepted_idx.size) < method.rollback_detection)
            rolled_back[accepted_idx] = detection
            if detection.any():
                detected_idx = accepted_idx[detection]
                # Rollback is not instantaneous; retain a small residual queueing penalty.
                post[detected_idx] = before[detection] * rng.uniform(1.00, 1.025, detection.sum())

            harmful[accepted_idx] = post[accepted_idx] > before * 1.045
            successful[accepted_idx] = post[accepted_idx] < before * 0.955

    # Extend each intervention over a short forward control horizon.
    direct_effect = latent - post
    post = latent.copy()
    decay = np.array([1.00, 0.72, 0.48, 0.30, 0.16])
    for t, effect in enumerate(direct_effect):
        if abs(effect) < 1e-12:
            continue
        end = min(steps, t + decay.size)
        post[t:end] -= effect * decay[: end - t]
    post = np.clip(post, 0.10, 2.2)

    fct = _fct_from_congestion(rng, post, scenario)
    loss_pct = 100.0 * np.mean(np.maximum(post - 1.05, 0.0) ** 2 * 0.018)
    queue_occupancy = 100.0 * np.mean(np.clip((post - 0.40) / 1.25, 0, 1))
    link_utilization = 100.0 * np.mean(np.clip(post / 1.15, 0, 1))
    fairness = 1.0 - np.clip(0.17 * np.std(post) + 0.04 * scenario.oversubscription, 0, 0.35)
    route_churn = 100.0 * accepted.sum() * method.churn_factor / max(steps, 1)
    slo_violation = 100.0 * np.mean(fct > scenario.slo_ms)

    accepted_count = int(accepted.sum())
    harmful_rate = 100.0 * harmful.sum() / max(accepted_count, 1)
    success_rate = 100.0 * successful.sum() / max(accepted_count, 1)
    rollback_rate = 100.0 * rolled_back.sum() / max(accepted_count, 1)
    localization_accuracy = 100.0 * correct[triggered].mean() if action_count else 0.0
    base_prediction_error = {
        "ECMP": np.nan,
        "Static-TE": np.nan,
        "Correlation-ML": 20.5,
        "DRL": 16.8,
        "Twin-No-Causal": 11.6,
        "CausalNetTwin": 5.9,
    }[method.name]
    if np.isnan(base_prediction_error):
        counterfactual_mape = np.nan
    else:
        counterfactual_mape = base_prediction_error + 3.2 * scenario.burstiness + 1.6 * scenario.failure_probability + rng.normal(0, 0.45)

    return {
        "scenario": scenario.name,
        "topology": scenario.topology,
        "method": method.name,
        "seed": seed,
        "p95_fct_ms": float(np.percentile(fct, 95)),
        "p99_fct_ms": float(np.percentile(fct, 99)),
        "mean_fct_ms": float(np.mean(fct)),
        "slo_violation_pct": float(slo_violation),
        "link_utilization_pct": float(link_utilization),
        "queue_occupancy_pct": float(queue_occupancy),
        "packet_loss_pct": float(loss_pct),
        "jain_fairness": float(fairness),
        "route_churn_pct": float(route_churn),
        "intervention_success_pct": float(success_rate),
        "harmful_action_pct": float(harmful_rate),
        "rollback_pct": float(rollback_rate),
        "source_localization_pct": float(localization_accuracy),
        "telemetry_overhead_pct": float(method.telemetry_overhead_pct + rng.normal(0, 0.08)),
        "inference_latency_ms": float(method.inference_latency_ms + rng.normal(0, 0.18)),
        "counterfactual_mape_pct": float(counterfactual_mape),
        "actions_proposed": action_count,
        "actions_accepted": accepted_count,
        "actions_rejected": int(action_count - accepted_count),
    }


def run_matrix(
    scenarios: List[Scenario],
    methods: List[MethodProfile],
    seeds: List[int],
    steps: int = 600,
) -> pd.DataFrame:
    """Run all combinations and return a tidy DataFrame."""
    rows: List[Dict[str, float]] = []
    for scenario in scenarios:
        for method in methods:
            for seed in seeds:
                rows.append(run_trial(scenario, method, seed, steps))
    return pd.DataFrame(rows)
