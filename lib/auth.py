"""Single shared-password gate with idle timeout (Streamlit session-state)."""
from __future__ import annotations
import hmac
import time
import streamlit as st
from lib import i18n

IDLE_TIMEOUT_MIN = 30


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
    st.title(i18n.t("app_title", lang))
    st.subheader(i18n.t("login_title", lang))
    pw = st.text_input(i18n.t("password", lang), type="password")
    if st.button(i18n.t("login_btn", lang)):
        if check_password(pw, st.secrets.get("APP_PASSWORD", "")):
            st.session_state["authenticated"] = True
            st.session_state["last_active"] = time.time()
            st.rerun()
        else:
            st.error(i18n.t("login_error", lang))
