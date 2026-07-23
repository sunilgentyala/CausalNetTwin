"""CausalNetTwin research artifact."""

from .config import METHODS, SCENARIOS
from .simulator import run_matrix, run_trial

__all__ = ["METHODS", "SCENARIOS", "run_matrix", "run_trial"]
