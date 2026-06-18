"""Orchestration: cached load_data() = fetch (kobo) + decode -> DataFrame."""
from __future__ import annotations
import pandas as pd
import streamlit as st
from lib import kobo, decode

# Indirection points so tests can monkeypatch without network/secrets:
_fetch_form = kobo.fetch_form
_fetch_submissions = kobo.fetch_submissions


def _read_config() -> kobo.KoboConfig:
    return kobo.KoboConfig.from_mapping(st.secrets)


@st.cache_data(ttl=300, show_spinner="ກຳລັງໂຫຼດຂໍ້ມູນ...")
def load_data() -> pd.DataFrame:
    cfg = _read_config()
    form = _fetch_form(cfg)
    subs = _fetch_submissions(cfg)
    return decode.decode_submissions(subs, form)


def clear_cache() -> None:
    load_data.clear()
