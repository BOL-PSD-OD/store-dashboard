import datetime as dt
from lib import decode

def test_decode_submissions(form, subs):
    df = decode.decode_submissions(subs, form)
    assert len(df) == 2
    # group prefix stripped + select_one decoded
    assert list(df["S3_Q1"]) == ["restaurant", "hotel"]
    assert list(df["S3_Q1_label"]) == ["ຮ້ານອາຫານ", "ໂຮງແຮມ"]
    # select_multiple -> list of codes + list of labels (PSP Lao QR is now S3_Q7)
    assert df.loc[0, "S3_Q7"] == ["1", "2"]
    assert df.loc[0, "S3_Q7_label"] == ["BCEL", "JDB"]
    # combined PSP column (across S3_Q7/Q8/Q10)
    assert df.loc[0, "_psp_label"] == ["BCEL", "JDB"]
    # derived account status (acquirer x use_domestic x interested)
    assert df.loc[0, "_status"] == "both_int"
    assert df.loc[1, "_status"] == "foreign_unint"
    # interview date (S0_Q1) formatted DD/MM/YYYY
    assert df.loc[0, "_idate_label"] == "29/06/2026"
    # submission date in Asia/Vientiane (UTC+7)
    assert df.loc[0, "_date"] == dt.date(2026, 6, 29)
    assert df.loc[1, "_date"] == dt.date(2026, 6, 29)

def test_stable_detail_columns_resolve_after_license_shift(form, subs):
    """district/village/nationality are exposed under renumber-proof _* columns
    resolved from the form, not the raw S3.1_Q* positions (which shifted when the
    2026-07 form inserted the License question at S3.1_Q1)."""
    df = decode.decode_submissions(subs, form)
    assert list(df["_district"]) == ["ຫຼວງພະບາງ", "ຈອມເພັດ"]
    assert df.loc[0, "_village"] == "ບ. ໜຶ່ງ"
    assert list(df["_nationality"]) == ["ລາວ", "ໄທ"]


def test_decode_empty(form):
    df = decode.decode_submissions([], form)
    assert len(df) == 0
    assert "S3_Q1_label" in df.columns  # columns still present for downstream charts
    assert "_status_label" in df.columns
    assert "_district" in df.columns and "_nationality" in df.columns
