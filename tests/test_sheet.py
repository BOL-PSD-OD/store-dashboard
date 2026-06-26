import json
from lib import sheet


def test_submissions_and_form_reconstructs():
    raw_rows = [
        {"uuid": "u1", "raw_json": json.dumps({"S3_Q1": "hotel", "_id": 1})},
        {"uuid": "u2", "raw_json": json.dumps({"S3_Q1": "restaurant", "_id": 2})},
        {"uuid": "", "raw_json": ""},   # blank row -> skipped
    ]
    form_rows = [{"form_json": json.dumps({"content": {"survey": [], "choices": []}})}]
    subs, form = sheet.submissions_and_form(raw_rows, form_rows)
    assert subs == [{"S3_Q1": "hotel", "_id": 1}, {"S3_Q1": "restaurant", "_id": 2}]
    assert form == {"content": {"survey": [], "choices": []}}


def test_submissions_and_form_empty():
    subs, form = sheet.submissions_and_form([], [])
    assert subs == [] and form == {}
