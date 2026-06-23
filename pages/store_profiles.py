"""Store Profiles page: filter, search, results table, full profile + map."""
import re
import streamlit as st
import pandas as pd
from lib import data, i18n

lang = st.session_state.get("lang", i18n.DEFAULT_LANG)
df = data.load_data()

st.title(i18n.t("nav_profiles", lang))

if df.empty:
    st.info(i18n.t("no_data", lang))
    st.stop()


def _name(row) -> str:
    for col in ("S3_Q2_oth", "S3_Q2_label", "S3_Q2"):
        v = row.get(col)
        if isinstance(v, str) and v.strip():
            return v
    return f"#{row.get('_id', '?')}"


df = df.copy()
df["_store_name"] = df.apply(_name, axis=1)

# --- Filters ---
all_txt = i18n.t("all", lang)
with st.sidebar:
    types = [all_txt] + sorted(df["S3_Q1_label"].dropna().unique().tolist())
    pick_type = st.selectbox(i18n.t("filter_biztype", lang), types)
    query = st.text_input(i18n.t("search_store", lang))

view = df
if pick_type != all_txt:
    view = view[view["S3_Q1_label"] == pick_type]
if query:
    view = view[view["_store_name"].str.contains(query, case=False, na=False)]

st.caption(i18n.t("results_count", lang).format(n=len(view)))

# --- Results table ---
show = view[["_store_name", "S3_Q1_label", "_status_label"]].rename(columns={
    "_store_name": i18n.t("search_store", lang),
    "S3_Q1_label": i18n.t("filter_biztype", lang),
    "_status_label": i18n.t("filter_status", lang),
})
st.dataframe(show, use_container_width=True, hide_index=True)

# --- Profile detail ---
st.subheader(i18n.t("select_store", lang))
names = view["_store_name"].tolist()
if names:
    picked = st.selectbox(i18n.t("select_store", lang), names, label_visibility="collapsed")
    row = view[view["_store_name"] == picked].iloc[0]
    qlabels = data.load_question_labels()  # ordered {code: label} from the live form

    def _isna(x):
        return x is None or (not isinstance(x, list) and pd.isna(x))

    def _value(code):
        """Human-readable answer: decoded label, joined multi-select, plus 'other' text."""
        val = row.get(code + "_label")
        if _isna(val):
            val = row.get(code)
        if isinstance(val, list):
            val = ", ".join(str(v) for v in val) if val else None
        if _isna(val):
            val = None
        oth = row.get(code + "_oth")
        if isinstance(oth, str) and oth.strip():
            val = f"{val} — {oth}" if val else oth
        return None if val in (None, "") else str(val)

    # Group questions by section number (S1_–S4_) in form order; *_oth merged above.
    sections = {"section_1": [], "section_2": [], "section_3": [], "section_4": []}
    for code, label in qlabels.items():
        if code.endswith("_oth"):
            continue
        m = re.match(r"S(\d)_", code)
        key = f"section_{m.group(1)}" if m else None
        if key in sections:
            sections[key].append((code, label))

    for sec_key, items in sections.items():
        if not items:
            continue
        with st.expander(i18n.t(sec_key, lang), expanded=(sec_key == "section_3")):
            for code, label in items:
                v = _value(code)
                if v is not None:
                    st.markdown(f"**{label}**  \n{v}")

    # Location map: geopoint question is "lat lon alt prec"; fall back to _geolocation.
    def _latlon(r):
        raw = r.get("geopoint")
        if isinstance(raw, str) and len(raw.split()) >= 2:
            a, b = raw.split()[:2]
            try:
                return float(a), float(b)
            except ValueError:
                pass
        g = r.get("_geolocation")
        if isinstance(g, list) and len(g) >= 2 and g[0] is not None and g[1] is not None:
            return float(g[0]), float(g[1])
        return r.get("_geopoint_latitude"), r.get("_geopoint_longitude")

    lat, lon = _latlon(row)
    if pd.notna(lat) and pd.notna(lon):
        st.map(pd.DataFrame({"lat": [float(lat)], "lon": [float(lon)]}))
