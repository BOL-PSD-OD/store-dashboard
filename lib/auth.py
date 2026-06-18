"""Single shared-password gate with idle timeout (Streamlit session-state)."""
from __future__ import annotations
import base64
import hmac
import time
from pathlib import Path
import streamlit as st
from lib import i18n

IDLE_TIMEOUT_MIN = 30
_LOGO = Path(__file__).resolve().parent.parent / "assets" / "BOL_Logo.png"


def _logo_html(width: int = 150) -> str:
    if not _LOGO.exists():
        return ""
    b64 = base64.b64encode(_LOGO.read_bytes()).decode()
    return (f"<div style='text-align:center;margin-bottom:0.5rem'>"
            f"<img src='data:image/png;base64,{b64}' width='{width}'></div>")


def check_password(entered: str, actual: str) -> bool:
    if not entered or not actual:
        return False
    return hmac.compare_digest(str(entered), str(actual))


def is_expired(last: float | None, now: float, timeout_min: int = IDLE_TIMEOUT_MIN) -> bool:
    if last is None:
        return True
    return (now - last) > timeout_min * 60


def is_authenticated() -> bool:
    if not st.session_state.get("authenticated"):
        return False
    if is_expired(st.session_state.get("last_active"), time.time()):
        st.session_state["authenticated"] = False
        return False
    st.session_state["last_active"] = time.time()
    return True


def logout() -> None:
    st.session_state["authenticated"] = False
    st.session_state.pop("last_active", None)


def login_page() -> None:
    lang = st.session_state.get("lang", i18n.DEFAULT_LANG)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(_logo_html(), unsafe_allow_html=True)
        st.markdown(
            f"<h2 style='text-align:center;margin:0'>{i18n.t('app_title', lang)}</h2>"
            f"<p style='text-align:center;color:#9aa7b4;margin-top:0.25rem'>"
            f"{i18n.t('login_title', lang)}</p>",
            unsafe_allow_html=True,
        )
        # st.form: pressing Enter in the password field submits (no need to click).
        with st.form("login_form"):
            pw = st.text_input(i18n.t("password", lang), type="password")
            submitted = st.form_submit_button(i18n.t("login_btn", lang),
                                              use_container_width=True)
        if submitted:
            if check_password(pw, st.secrets.get("APP_PASSWORD", "")):
                st.session_state["authenticated"] = True
                st.session_state["last_active"] = time.time()
                st.rerun()
            else:
                st.error(i18n.t("login_error", lang))
