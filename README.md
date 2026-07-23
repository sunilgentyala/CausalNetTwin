<p align="center">
  <img src="docs/assets/logo-512.png" width="96" alt="CausalNetTwin logo">
</p>

<h1 align="center">CausalNetTwin</h1>
<p align="center"><b>A Counterfactual Network Digital Twin for Safe Agentic Remediation in Multi-Tenant AI Data-Center Fabrics</b></p>

<p align="center">
  <a href="https://sunilgentyala.github.io/CausalNetTwin/"><img src="https://img.shields.io/badge/site-live-38bdf8" alt="Site"></a>
  <img src="https://img.shields.io/badge/paper-IEEE%20INFOCOM%202027%20(submitted)-fbbf24" alt="Paper status">
  <img src="https://img.shields.io/badge/license-Apache%202.0-22c55e" alt="License">
  <img src="https://img.shields.io/badge/tests-6%20passing-22c55e" alt="Tests">
  <img src="https://img.shields.io/badge/trials-1%2C080%20reproducible-a78bfa" alt="Trials">
</p>

**Site:** https://sunilgentyala.github.io/CausalNetTwin/

CausalNetTwin is a reproducible research artifact for evaluating counterfactual, safety-constrained remediation in multi-tenant AI data-center fabrics. Before a routing, queue, ECN, or rate-control action reaches production, the twin estimates its outcome under an explicit `do(A=a)` intervention, rejects any candidate that violates configured tail-latency, loss, fairness, churn, or SLO limits, and verifies + rolls back after deployment if observed behavior diverges from the approved prediction. The repository contains a lightweight structural simulator, safety contracts, rollback verification, tests, experiment configurations, and generated results. The IEEE manuscript is intentionally not stored in this repository.

## Headline result

Across 1,080 method-scenario-seed trials (6 methods × 6 workload/failure scenarios × 30 seeds), CausalNetTwin records **4.50 ms P95 / 8.19 ms P99** flow-completion time, a 61.4% reduction in P99 versus ECMP, while cutting harmful accepted actions from 10.30% (non-causal twin baseline) to **0.03%**. Full tables and the reproduction command are on the [site](https://sunilgentyala.github.io/CausalNetTwin/#results).

## Core capabilities

- Models mixed AI AllReduce, storage replication, Kafka, Spark shuffle, and latency-sensitive traffic.
- Compares ECMP, static traffic engineering, correlation-based ML, conventional DRL, a non-causal digital twin, and CausalNetTwin.
- Rejects candidate actions that violate tail-latency, packet-loss, fairness, route-churn, or SLO limits.
- Verifies observed post-deployment behavior and triggers rollback when outcomes materially deviate from counterfactual predictions.
- Produces repeatable CSV results and 95% confidence intervals from fixed random seeds.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m pytest -q
python -m causalnettwin.cli --output results --seeds 30 --steps 600
```

Windows PowerShell users can run `scripts/run_all.ps1`. Linux and macOS users can run `scripts/run_all.sh`.

## Repository layout

- `src/causalnettwin/`: simulator, safety gate, statistical analysis, and rollback logic
- `experiments/`: reproducible benchmark entry point and configuration
- `tests/`: unit and reproducibility tests
- `results/`: trial data, summaries, confidence intervals, and test output
- `docs/`: architecture, telemetry schema, experiment method, safety contract, and novelty review
- `diagrams/`: repository documentation figures

## Scope statement

The included benchmark is a deterministic structural and event-driven research simulator. It is suitable for testing causal logic, safety policies, reproducibility, and comparative trends. It is not a replacement for packet-level validation in ns-3, BMv2/P4, Containerlab, Mininet, or a hardware testbed. The experiment plan in `docs/experiment_design.md` defines how to extend the artifact to those platforms.

## Authors

| Author | Affiliation |
|---|---|
| **Sunil Gentyala** *(corresponding author)* | HCLTech |
| **Suresh Kumar Darisi** | Rocket Software |
| **John Martin** | HCLTech, Auckland, New Zealand |
| **Floriano Caprio** | Università Campus Bio-Medico di Roma |

## License

Apache License 2.0. See `LICENSE`.
