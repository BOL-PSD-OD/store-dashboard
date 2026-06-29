import pandas as pd
from lib import psp, decode


def test_psp_dataframe_empty_is_empty():
    assert psp.psp_dataframe([]).empty


def test_interest_series_maps_status_to_short_buckets(form, subs):
    df = decode.decode_submissions(subs, form)   # sub1 both_int, sub2 foreign_unint
    s = psp.interest_series(df)
    assert int(s.get("ສົນໃຈ", 0)) == 1
    assert int(s.get("ບໍ່ສົນໃຈ", 0)) == 1


def test_result_series_three_buckets():
    pdf = pd.DataFrame({"last_result": ["ເປີດ", "ບໍ່ເປີດ", "", "ເປີດ"]})
    s = psp.result_series(pdf)
    assert int(s.get("🟢 ເປີດ", 0)) == 2
    assert int(s.get("🔵 ໄປແລ້ວ·ບໍ່ເປີດ", 0)) == 1
    assert int(s.get("⚪ ຍັງບໍ່ໄປ", 0)) == 1


def test_by_bank_groups_opened_vs_pending():
    pdf = pd.DataFrame({
        "PSP": ["BCEL", "BCEL", "LDB", "LDB"],
        "last_result": ["ເປີດ", "ບໍ່ເປີດ", "ເປີດ", ""],
    })
    long = psp.by_bank(pdf)

    def cell(p, c):
        m = long[(long["provider"] == p) & (long["context"] == c)]
        return int(m["count"].sum())

    assert cell("BCEL", "ເປີດ") == 1 and cell("BCEL", "ຍັງ") == 1
    assert cell("LDB", "ເປີດ") == 1 and cell("LDB", "ຍັງ") == 1


def test_kpis_counts_and_conversion(form, subs):
    df = decode.decode_submissions(subs, form)   # surveyed=2, interested=1 (both_int)
    pdf = pd.DataFrame({"PSP": ["BCEL", "BCEL", "LDB"],
                        "last_result": ["ເປີດ", "ບໍ່ເປີດ", ""]})  # followed=2 opened=1
    k = psp.kpis(df, pdf)
    assert k["surveyed"] == 2 and k["interested"] == 1
    assert k["followed_up"] == 2 and k["opened"] == 1
    assert k["conv_followed"] == 50.0
    assert k["conv_overall"] == 100.0


def test_kpis_no_divide_by_zero():
    df = pd.DataFrame({"_status": []})
    k = psp.kpis(df, psp.psp_dataframe([]))
    assert k["conv_followed"] == 0.0 and k["conv_overall"] == 0.0


def test_load_psp_data_reads_rows(monkeypatch):
    from lib import data
    monkeypatch.setattr(data, "_read_psp_config", lambda: ("sid", {"sa_json": "x"}))
    monkeypatch.setattr(data, "_fetch_psp",
                        lambda sid, auth: [{"PSP": "BCEL", "store_id": "H001", "last_result": "ເປີດ"}])
    df = data.load_psp_data.__wrapped__()
    assert len(df) == 1 and df.iloc[0]["PSP"] == "BCEL"


def test_load_psp_data_resilient_on_error(monkeypatch):
    from lib import data

    def boom():
        raise KeyError("PSP_SHEET_ID")

    monkeypatch.setattr(data, "_read_psp_config", boom)
    assert data.load_psp_data.__wrapped__().empty
