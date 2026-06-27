"""Orchestration: cached load_data() = fetch from Sheet (_raw/_form) + decode."""
from __future__ import annotations
import pandas as pd
import streamlit as st
from lib import sheet, decode

# Indirection point so tests can monkeypatch without network/secrets:
_fetch = sheet.fetch


def _read_config():
    """Return (sheet_id, auth). Prefer user OAuth (the user owns the Sheet; the
    service account was deleted) and fall back to the service account."""
    sid = str(st.secrets["SHEET_ID"])
    if st.secrets.get("GOOGLE_OAUTH_CLIENT_ID"):
        auth = {"client_id": str(st.secrets["GOOGLE_OAUTH_CLIENT_ID"]),
                "client_secret": str(st.secrets["GOOGLE_OAUTH_CLIENT_SECRET"]),
                "refresh_token": str(st.secrets["GOOGLE_OAUTH_REFRESH_TOKEN"])}
    else:
        auth = {"sa_json": str(st.secrets["GOOGLE_SA_JSON"])}
    return sid, auth


@st.cache_data(ttl=300, show_spinner="ກຳລັງໂຫຼດຂໍ້ມູນ...")
def load_data() -> pd.DataFrame:
    sid, auth = _read_config()
    subs, form = _fetch(sid, auth)
    return decode.decode_submissions(subs, form)


@st.cache_data(ttl=600)
def load_question_labels() -> dict:
    sid, auth = _read_config()
    _, form = _fetch(sid, auth)
    return decode.build_question_labels(form)


def clear_cache() -> None:
    load_data.clear()
    load_question_labels.clear()
