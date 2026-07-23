#!/usr/bin/env bash
set -euo pipefail
python -m pytest -q
python -m causalnettwin.cli --output results --seeds 30 --steps 600
