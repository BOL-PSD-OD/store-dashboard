"""Map page: embeds the kobo-live-map (Leaflet map on GitHub Pages)."""
import streamlit as st
import streamlit.components.v1 as components
from lib import i18n

MAP_URL = "https://panngeun.github.io/kobo-live-map/"

lang = st.session_state.get("lang", i18n.DEFAULT_LANG)
st.title(i18n.t("nav_map", lang))
st.link_button(i18n.t("map_open_newtab", lang), MAP_URL)  # button → opens map in a new tab
components.iframe(MAP_URL, height=760, scrolling=True)
