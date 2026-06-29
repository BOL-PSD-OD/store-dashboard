"""Entry point: language toggle, auth gate, navigation to the two pages."""
import streamlit as st
from lib import auth, i18n, data

st.set_page_config(page_title="Store Survey Dashboard", page_icon="🏪", layout="wide")

# Fonts: Latin/digits -> Times New Roman, Lao glyphs -> Phetsarath (font fallback).
# Re-apply the Material icon font so Streamlit UI icons keep working.
FONT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Phetsarath:wght@400;700&display=swap');
.stApp, .stApp * { font-family: 'Times New Roman', 'Phetsarath', serif !important; }
.stApp [data-testid="stIconMaterial"],
.stApp [class*="material-symbols"] { font-family: 'Material Symbols Rounded' !important; }
</style>
"""
st.markdown(FONT_CSS, unsafe_allow_html=True)

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
        st.Page("pages/compare.py", title=i18n.t("nav_compare", lang), icon="⚖️"),
        st.Page("pages/store_profiles.py", title=i18n.t("nav_profiles", lang), icon="🏪"),
        st.Page("pages/map.py", title=i18n.t("nav_map", lang), icon="🗺️"),
    ])
    nav.run()
