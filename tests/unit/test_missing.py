from easy_addoption.missing import MISSING


def test_missing_bool():
    assert not MISSING  # MISSING represents False


def test_missing_repr():
    assert repr(MISSING) == "Missing()"
