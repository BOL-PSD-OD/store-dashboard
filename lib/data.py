"""Orchestration: cached load_data() = fetch from Sheet (_raw/_form) + decode."""
from __future__ import annotations
import pandas as pd
import streamlit as st
from lib import sheet, decode

# Indirection point so tests can monkeypatch without network/secrets:
_fetch = sheet.fetch


def _read_config():
    return str(st.secrets["SHEET_ID"]), str(st.secrets["GOOGLE_SA_JSON"])


@st.cache_data(ttl=300, show_spinner="ກຳລັງໂຫຼດຂໍ້ມູນ...")
def load_data() -> pd.DataFrame:
    sid, sa = _read_config()
    subs, form = _fetch(sid, sa)
    return decode.decode_submissions(subs, form)


@st.cache_data(ttl=600)
def load_question_labels() -> dict:
    sid, sa = _read_config()
    _, form = _fetch(sid, sa)
    return decode.build_question_labels(form)


def clear_cache() -> None:
    load_data.clear()
    load_question_labels.clear()
