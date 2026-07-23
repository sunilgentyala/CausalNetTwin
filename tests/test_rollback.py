from causalnettwin.rollback import VerificationWindow, should_rollback


def test_rollback_on_large_tail_deviation():
    assert should_rollback(VerificationWindow(8.0, 11.0, 0.05, 0.05))


def test_no_rollback_when_outcome_matches_prediction():
    assert not should_rollback(VerificationWindow(8.0, 8.5, 0.05, 0.052))
