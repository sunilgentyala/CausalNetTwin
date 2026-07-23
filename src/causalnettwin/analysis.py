"""Statistical aggregation for CausalNetTwin experiments."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats


METRICS = [
    "p95_fct_ms",
    "p99_fct_ms",
    "mean_fct_ms",
    "slo_violation_pct",
    "link_utilization_pct",
    "queue_occupancy_pct",
    "packet_loss_pct",
    "jain_fairness",
    "route_churn_pct",
    "intervention_success_pct",
    "harmful_action_pct",
    "rollback_pct",
    "source_localization_pct",
    "telemetry_overhead_pct",
    "inference_latency_ms",
    "counterfactual_mape_pct",
]


def mean_ci(values: Iterable[float], confidence: float = 0.95) -> tuple[float, float, float]:
    """Return mean and Student-t confidence interval."""
    arr = np.asarray(list(values), dtype=float)
    mean = float(arr.mean())
    if arr.size < 2:
        return mean, mean, mean
    sem = stats.sem(arr)
    half = float(stats.t.ppf((1 + confidence) / 2, arr.size - 1) * sem)
    return mean, mean - half, mean + half


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Create method-level means across scenarios and seeds."""
    return (
        df.groupby("method", sort=False)[METRICS]
        .mean(numeric_only=True)
        .reset_index()
    )


def scenario_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create scenario-by-method summaries."""
    return (
        df.groupby(["scenario", "method"], sort=False)[METRICS]
        .mean(numeric_only=True)
        .reset_index()
    )


def confidence_intervals(df: pd.DataFrame) -> pd.DataFrame:
    """Create confidence intervals for the main outcome metrics."""
    rows = []
    for method, group in df.groupby("method", sort=False):
        for metric in ["p95_fct_ms", "p99_fct_ms", "slo_violation_pct", "harmful_action_pct"]:
            mean, low, high = mean_ci(group[metric])
            rows.append({"method": method, "metric": metric, "mean": mean, "ci95_low": low, "ci95_high": high})
    return pd.DataFrame(rows)
