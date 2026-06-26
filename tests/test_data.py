from lib import data


def test_load_data_reads_sheet_and_decodes(monkeypatch, form, subs):
    monkeypatch.setattr(data, "_read_config", lambda: ("sid", "sa"))
    monkeypatch.setattr(data, "_fetch", lambda sid, sa: (subs, form))
    df = data.load_data.__wrapped__()   # bypass st.cache_data
    assert len(df) == 2
    assert list(df["S3_Q1_label"]) == ["ຮ້ານອາຫານ", "ໂຮງແຮມ"]


def test_load_question_labels(monkeypatch, form):
    monkeypatch.setattr(data, "_read_config", lambda: ("sid", "sa"))
    monkeypatch.setattr(data, "_fetch", lambda sid, sa: ([], form))
    labels = data.load_question_labels.__wrapped__()
    assert labels["S3_Q1"] == "3.1 biz type"
