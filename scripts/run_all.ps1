$ErrorActionPreference = "Stop"
python -m pytest -q
python -m causalnettwin.cli --output results --seeds 30 --steps 600
