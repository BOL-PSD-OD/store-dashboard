"""Read submissions + form from the sync Google Sheet (read-only service account)."""
from __future__ import annotations
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def submissions_and_form(raw_rows: list[dict], form_chunks: list[str]):
    """Pure: rebuild (submissions, form) from _raw rows + the _form column-A chunks.
    The form JSON is stored split across cells (Sheets' 50k-char/cell limit)."""
    subs = [json.loads(r["raw_json"]) for r in raw_rows if r.get("raw_json")]
    form_json = "".join(str(c) for c in form_chunks)
    form = json.loads(form_json) if form_json else {}
    return subs, form


def fetch(sheet_id: str, sa_json: str):
    # gspread/google-auth imported lazily so the pure helper above stays import-free.
    import gspread
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_info(json.loads(sa_json), scopes=SCOPES)
    sh = gspread.authorize(creds).open_by_key(sheet_id)
    raw_rows = sh.worksheet("_raw").get_all_records()
    try:
        form_chunks = sh.worksheet("_form").col_values(1)[1:]   # column A, skip "form_json" header
    except gspread.WorksheetNotFound:
        form_chunks = []
    return submissions_and_form(raw_rows, form_chunks)
