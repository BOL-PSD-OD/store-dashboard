import datetime as dt
from lib import decode

def test_decode_submissions(form, subs):
    df = decode.decode_submissions(subs, form)
    assert len(df) == 2
    # group prefix stripped + select_one decoded
    assert list(df["S3_Q1"]) == ["restaurant", "hotel"]
    assert list(df["S3_Q1_label"]) == ["ຮ້ານອາຫານ", "ໂຮງແຮມ"]
    # select_multiple -> list of codes + list of labels
    assert df.loc[0, "S3_Q10"] == ["1", "2"]
    assert df.loc[0, "S3_Q10_label"] == ["BCEL", "JDB"]
    # combined PSP column (across S3_Q10/Q11/Q13)
    assert df.loc[0, "_psp_label"] == ["BCEL", "JDB"]
    # derived account status (acquirer x use_domestic x interested)
    assert df.loc[0, "_status"] == "both_int"
    assert df.loc[1, "_status"] == "foreign_unint"
    # interview date (S0_Q1) formatted DD/MM/YYYY
    assert df.loc[0, "_idate_label"] == "29/06/2026"
    # submission date in Asia/Vientiane (UTC+7)
    assert df.loc[0, "_date"] == dt.date(2026, 6, 29)
    assert df.loc[1, "_date"] == dt.date(2026, 6, 29)

def test_decode_empty(form):
    df = decode.decode_submissions([], form)
    assert len(df) == 0
    assert "S3_Q1_label" in df.columns  # columns still present for downstream charts
    assert "_status_label" in df.columns
