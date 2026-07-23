"""Command-line entry point for the reproducible benchmark."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import confidence_intervals, scenario_summary, summarize
from .config import METHODS, SCENARIOS
from .simulator import run_matrix


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the CausalNetTwin benchmark")
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--steps", type=int, default=600)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    df = run_matrix(list(SCENARIOS), list(METHODS), list(range(args.seeds)), args.steps)
    df.to_csv(args.output / "trial_results.csv", index=False)
    summarize(df).to_csv(args.output / "benchmark_summary.csv", index=False)
    scenario_summary(df).to_csv(args.output / "scenario_results.csv", index=False)
    confidence_intervals(df).to_csv(args.output / "confidence_intervals.csv", index=False)
    print(f"Wrote results to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
