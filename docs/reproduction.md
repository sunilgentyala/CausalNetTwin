# Reproduction Notes

The checked-in results were generated with 30 seeds, 600 control windows per trial, six scenarios, and six methods. This produces 1,080 trial summaries.

```bash
pip install -e ".[dev]"
pytest -q
python -m causalnettwin.cli --output results --seeds 30 --steps 600
```

Expected test result: `6 passed`.

The simulator uses NumPy's `default_rng` and records every seed in `results/trial_results.csv`. Re-running the command with the same software versions and arguments produces identical trial records.
