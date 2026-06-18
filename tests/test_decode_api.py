"""Decode against the REAL Kobo asset-content shape: type='select_one' plus a
separate 'select_from_list_name' key (not the XLSForm combined 'select_one X')."""
import pytest
from lib import decode, charts

API_FORM = {
    "content": {
        "survey": [
            {"type": "begin_group", "name": "Section_2"},
            {"type": "select_one", "select_from_list_name": "biz_type",
             "name": "S2_Q1", "label": ["2.1 ປະເພດທຸລະກິດ"]},
            {"type": "select_multiple", "select_from_list_name": "psp",
             "name": "S2_Q8", "label": ["2.8 ທະນາຄານ/ຜູ້ໃຫ້ບໍລິການ"]},
            {"type": "select_one", "select_from_list_name": "date",
             "name": "S1_Q5", "label": ["1.5 ວັນທີໃຫ້ສໍາພາດ"]},
            {"type": "select_one", "select_from_list_name": "learn",
             "name": "S3_Q1", "label": ["3.1 ເຄີຍຮັບຮູ້ບໍ"]},
            {"type": "end_group"},
        ],
        "choices": [
            {"list_name": "biz_type", "name": "restaurant", "label": ["ຮ້ານອາຫານ"]},
            {"list_name": "biz_type", "name": "hotel", "label": ["ໂຮງແຮມ"]},
            {"list_name": "psp", "name": "1", "label": ["BCEL"]},
            {"list_name": "psp", "name": "2", "label": ["JDB"]},
            {"list_name": "date", "name": "1", "label": ["29/06/2026"]},
            {"list_name": "date", "name": "2", "label": ["30/06/2026"]},
            {"list_name": "learn", "name": "1", "label": ["ເຄີຍ"]},
        ],
    }
}

API_SUBS = [
    {"Section_2/S2_Q1": "restaurant", "S2_Q8": "1 2", "S1_Q5": "2", "S3_Q1": "1",
     "_submission_time": "2026-06-30T03:00:00", "_id": 1},
    {"Section_2/S2_Q1": "hotel", "S2_Q8": "1", "S1_Q5": "1", "S3_Q1": "0",
     "_submission_time": "2026-06-29T03:00:00", "_id": 2},
]


def test_select_one_decoded_via_select_from_list_name():
    df = decode.decode_submissions(API_SUBS, API_FORM)
    assert list(df["S2_Q1_label"]) == ["ຮ້ານອາຫານ", "ໂຮງແຮມ"]


def test_select_multiple_decoded_to_provider_names():
    df = decode.decode_submissions(API_SUBS, API_FORM)
    assert df.loc[0, "S2_Q8_label"] == ["BCEL", "JDB"]
    assert df.loc[1, "S2_Q8_label"] == ["BCEL"]


def test_interview_date_decoded():
    df = decode.decode_submissions(API_SUBS, API_FORM)
    assert list(df["S1_Q5_label"]) == ["30/06/2026", "29/06/2026"]


def test_build_question_labels_ordered():
    labels = decode.build_question_labels(API_FORM)
    assert labels["S2_Q1"] == "2.1 ປະເພດທຸລະກິດ"
    assert "Section_2" not in labels  # groups excluded
    assert list(labels.keys()) == ["S2_Q1", "S2_Q8", "S1_Q5", "S3_Q1"]  # survey order


def test_interview_date_counts_chronological():
    df = decode.decode_submissions(API_SUBS, API_FORM)
    counts = charts.interview_date_counts(df)
    assert list(counts.index) == ["29/06/2026", "30/06/2026"]  # ordered by real date
    assert counts["29/06/2026"] == 1 and counts["30/06/2026"] == 1


def test_psp_bar_uses_provider_names():
    df = decode.decode_submissions(API_SUBS, API_FORM)
    counts = charts.count_multi(df, "S2_Q8_label")
    assert counts["BCEL"] == 2
    assert counts["JDB"] == 1
