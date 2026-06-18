import datetime as dt
from lib import decode

def test_decode_submissions(form, subs):
    df = decode.decode_submissions(subs, form)
    assert len(df) == 2
    # group prefix stripped + select_one decoded
    assert list(df["S2_Q1"]) == ["restaurant", "hotel"]
    assert list(df["S2_Q1_label"]) == ["ຮ້ານອາຫານ", "ໂຮງແຮມ"]
    # select_multiple -> list of codes + list of labels
    assert df.loc[0, "S2_Q8"] == ["1", "2"]
    assert df.loc[0, "S2_Q8_label"] == ["BCEL", "JDB"]
    # submission date in Asia/Vientiane (UTC+7)
    assert df.loc[0, "_date"] == dt.date(2026, 6, 29)
    assert df.loc[1, "_date"] == dt.date(2026, 6, 29)

def test_decode_empty(form):
    df = decode.decode_submissions([], form)
    assert len(df) == 0
    assert "S2_Q1_label" in df.columns  # columns still present for downstream charts
