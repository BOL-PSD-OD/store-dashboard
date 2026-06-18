"""Entry point: language toggle, auth gate, navigation to the two pages."""
import streamlit as st
from lib import auth, i18n, data

st.set_page_config(page_title="Store Survey Dashboard", page_icon="🏪", layout="wide")

if "lang" not in st.session_state:
    st.session_state["lang"] = i18n.DEFAULT_LANG


def _sidebar_controls():
    lang = st.session_state["lang"]
    with st.sidebar:
        choice = st.radio(i18n.t("language", lang), ["ລາວ", "English"],
                          index=0 if lang == "lo" else 1, horizontal=True)
        st.session_state["lang"] = "lo" if choice == "ລາວ" else "en"
        if st.button(i18n.t("refresh", lang)):
            data.clear_cache()
            st.rerun()
        if st.button(i18n.t("logout", lang)):
            auth.logout()
            st.rerun()


if not auth.is_authenticated():
    st.navigation([st.Page(auth.login_page, title="Login")], position="hidden").run()
else:
    _sidebar_controls()
    lang = st.session_state["lang"]
    nav = st.navigation([
        st.Page("pages/dashboard.py", title=i18n.t("nav_dashboard", lang), icon="📊", default=True),
        st.Page("pages/store_profiles.py", title=i18n.t("nav_profiles", lang), icon="🏪"),
    ])
    nav.run()
