"""Read submissions + form from the sync Google Sheet (read-only service account)."""
from __future__ import annotations
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def submissions_and_form(raw_rows: list[dict], form_rows: list[dict]):
    """Pure: rebuild (submissions, form) from the _raw and _form tab rows."""
    subs = [json.loads(r["raw_json"]) for r in raw_rows if r.get("raw_json")]
    form = json.loads(form_rows[0]["form_json"]) if form_rows and form_rows[0].get("form_json") else {}
    return subs, form


def fetch(sheet_id: str, sa_json: str):
    # gspread/google-auth imported lazily so the pure helper above stays import-free.
    import gspread
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_info(json.loads(sa_json), scopes=SCOPES)
    sh = gspread.authorize(creds).open_by_key(sheet_id)
    raw_rows = sh.worksheet("_raw").get_all_records()
    try:
        form_rows = sh.worksheet("_form").get_all_records()
    except gspread.WorksheetNotFound:
        form_rows = []
    return submissions_and_form(raw_rows, form_rows)
