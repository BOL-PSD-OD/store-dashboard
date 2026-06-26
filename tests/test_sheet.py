import json
from lib import sheet


def test_submissions_and_form_reconstructs_from_chunks():
    raw_rows = [
        {"uuid": "u1", "raw_json": json.dumps({"S3_Q1": "hotel", "_id": 1})},
        {"uuid": "u2", "raw_json": json.dumps({"S3_Q1": "restaurant", "_id": 2})},
        {"uuid": "", "raw_json": ""},   # blank row -> skipped
    ]
    full = json.dumps({"content": {"survey": [], "choices": [{"x": "y"}]}})
    form_chunks = [full[i:i + 10] for i in range(0, len(full), 10)]   # split as the sync writes it
    subs, form = sheet.submissions_and_form(raw_rows, form_chunks)
    assert subs == [{"S3_Q1": "hotel", "_id": 1}, {"S3_Q1": "restaurant", "_id": 2}]
    assert form == {"content": {"survey": [], "choices": [{"x": "y"}]}}


def test_submissions_and_form_empty():
    subs, form = sheet.submissions_and_form([], [])
    assert subs == [] and form == {}
