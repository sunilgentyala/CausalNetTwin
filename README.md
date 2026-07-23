# CausalNetTwin

CausalNetTwin is a reproducible research artifact for evaluating counterfactual, safety-constrained remediation in multi-tenant AI data-center fabrics. The repository contains a lightweight structural simulator, safety contracts, rollback verification, tests, experiment configurations, and generated results. The IEEE manuscript is intentionally not stored in this repository.

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

Sunil Gentyala, corresponding author; Suresh Kumar Darisi; John Martin, HCLTech, Auckland, New Zealand; Floriano Caprio, Università Campus Bio-Medico di Roma.

## License

Apache License 2.0. See `LICENSE`.
