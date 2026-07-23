from causalnettwin.config import METHOD_MAP, SCENARIO_MAP
from causalnettwin.simulator import run_trial


def test_same_seed_is_reproducible():
    a = run_trial(SCENARIO_MAP["backup_ai_collision"], METHOD_MAP["CausalNetTwin"], seed=7, steps=200)
    b = run_trial(SCENARIO_MAP["backup_ai_collision"], METHOD_MAP["CausalNetTwin"], seed=7, steps=200)
    assert a == b


def test_causal_policy_reduces_tail_latency_against_ecmp():
    scenario = SCENARIO_MAP["oversubscribed_multi_tenant"]
    ecmp = run_trial(scenario, METHOD_MAP["ECMP"], seed=11, steps=400)
    causal = run_trial(scenario, METHOD_MAP["CausalNetTwin"], seed=11, steps=400)
    assert causal["p99_fct_ms"] < ecmp["p99_fct_ms"]
