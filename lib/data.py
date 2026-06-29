"""Orchestration: cached load_data() = fetch from Sheet (_raw/_form) + decode."""
from __future__ import annotations
import pandas as pd
import streamlit as st
from lib import sheet, decode, psp

# Indirection point so tests can monkeypatch without network/secrets:
_fetch = sheet.fetch
_fetch_psp = psp.fetch_psp


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


def _read_psp_config():
    """(PSP_SHEET_ID, auth) — reuses the same auth as the main Sheet."""
    _, auth = _read_config()
    return str(st.secrets["PSP_SHEET_ID"]), auth


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


@st.cache_data(ttl=300, show_spinner="ກຳລັງໂຫຼດຂໍ້ມູນ PSP...")
def load_psp_data() -> pd.DataFrame:
    """Round-2 follow-up frame. Empty (page stays alive) if PSP_SHEET_ID is unset
    or the read fails."""
    try:
        sid, auth = _read_psp_config()
        rows = _fetch_psp(sid, auth)
    except Exception:
        rows = []
    return psp.psp_dataframe(rows)


def clear_cache() -> None:
    load_data.clear()
    load_question_labels.clear()
    load_psp_data.clear()
