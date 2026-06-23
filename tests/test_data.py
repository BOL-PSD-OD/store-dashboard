from lib import data, kobo

def test_load_data_joins_fetch_and_decode(monkeypatch, form, subs):
    cfg = kobo.KoboConfig(token="t", uid="u", server="https://k")
    monkeypatch.setattr(data, "_read_config", lambda: cfg)
    monkeypatch.setattr(data, "_fetch_form", lambda c: form)
    monkeypatch.setattr(data, "_fetch_submissions", lambda c: subs)
    df = data.load_data.__wrapped__()  # call underlying fn, bypass st.cache_data
    assert len(df) == 2
    assert list(df["S3_Q1_label"]) == ["ຮ້ານອາຫານ", "ໂຮງແຮມ"]


def test_load_question_labels(monkeypatch, form):
    cfg = kobo.KoboConfig(token="t", uid="u", server="https://k")
    monkeypatch.setattr(data, "_read_config", lambda: cfg)
    monkeypatch.setattr(data, "_fetch_form", lambda c: form)
    labels = data.load_question_labels.__wrapped__()
    assert labels["S3_Q1"] == "3.1 biz type"
