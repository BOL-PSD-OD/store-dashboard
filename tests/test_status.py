import pytest
from lib.decode import derive_status, STATUS_LABELS, IN_SYSTEM


@pytest.mark.parametrize("acquirer,use_domestic,interested,expected", [
    # both domestic + foreign ("1" + "2")
    (["1", "2"], "1", None, "both_using"),
    (["1", "2"], "0", "1", "both_int"),
    (["1", "2"], "0", "0", "both_unint"),
    # foreign only ("2")
    (["2"], "1", None, "foreign_using"),
    (["2"], "0", "1", "foreign_int"),
    (["2"], "0", "0", "foreign_unint"),
    # domestic only ("1")
    (["1"], None, None, "domestic"),
    # no payment tool ("3")
    (["3"], None, "1", "notool_int"),
    (["3"], None, "0", "notool_unint"),
    # legacy/deployed form: foreign is "0", not "2"
    (["0"], "0", "1", "foreign_int"),
    (["1", "0"], "0", "0", "both_unint"),
    # nothing -> unknown
    ([], None, None, "unknown"),
])
def test_derive_status(acquirer, use_domestic, interested, expected):
    assert derive_status(acquirer, use_domestic, interested) == expected


def test_every_status_has_a_label():
    keys = {"domestic", "both_using", "foreign_using", "both_int", "foreign_int",
            "notool_int", "both_unint", "foreign_unint", "notool_unint", "unknown"}
    assert keys <= set(STATUS_LABELS)


def test_in_system_subset():
    assert set(IN_SYSTEM) <= set(STATUS_LABELS)
