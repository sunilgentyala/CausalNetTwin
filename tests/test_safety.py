from causalnettwin.safety import PredictedOutcome, approve


def test_safe_action_is_approved():
    ok, reasons = approve(PredictedOutcome(8.5, 0.04, 0.93, 0.8, 3.2))
    assert ok
    assert reasons == []


def test_risky_action_is_rejected():
    ok, reasons = approve(PredictedOutcome(14.0, 0.28, 0.80, 2.5, 10.0))
    assert not ok
    assert len(reasons) == 5
