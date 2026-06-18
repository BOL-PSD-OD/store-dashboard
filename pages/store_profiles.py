"""Store Profiles page: filter, search, results table, full profile + map."""
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
    for col in ("S2_Q2_oth", "S2_Q2_label", "S2_Q2"):
        v = row.get(col)
        if isinstance(v, str) and v.strip():
            return v
    return f"#{row.get('_id', '?')}"


df = df.copy()
df["_store_name"] = df.apply(_name, axis=1)

# --- Filters ---
all_txt = i18n.t("all", lang)
with st.sidebar:
    types = [all_txt] + sorted(df["S2_Q1_label"].dropna().unique().tolist())
    pick_type = st.selectbox(i18n.t("filter_biztype", lang), types)
    query = st.text_input(i18n.t("search_store", lang))

view = df
if pick_type != all_txt:
    view = view[view["S2_Q1_label"] == pick_type]
if query:
    view = view[view["_store_name"].str.contains(query, case=False, na=False)]

st.caption(i18n.t("results_count", lang).format(n=len(view)))

# --- Results table ---
show = view[["_store_name", "S2_Q1_label", "S2_Q7_label"]].rename(columns={
    "_store_name": i18n.t("search_store", lang),
    "S2_Q1_label": i18n.t("filter_biztype", lang),
    "S2_Q7_label": i18n.t("filter_status", lang),
})
st.dataframe(show, use_container_width=True, hide_index=True)

# --- Profile detail ---
st.subheader(i18n.t("select_store", lang))
names = view["_store_name"].tolist()
if names:
    picked = st.selectbox(i18n.t("select_store", lang), names, label_visibility="collapsed")
    row = view[view["_store_name"] == picked].iloc[0]

    sections = {
        "section_1": ["S1_Q1", "S1_Q2", "S1_Q3", "S1_Q4"],
        "section_2": ["S2_Q1", "S2_Q3", "S2_Q4", "S2_Q5", "S2_Q6", "S2_Q7",
                      "S2_Q8", "S2_Q9", "S2_Q10", "S2_Q11", "S2_Q12", "S2_Q13"],
        "section_3": ["S3_Q1", "S3_Q2", "S3_Q3", "S3_Q4", "S3_Q5"],
    }
    for sec_key, codes in sections.items():
        with st.expander(i18n.t(sec_key, lang), expanded=(sec_key == "section_2")):
            for code in codes:
                label_col = code + "_label"
                if label_col in row and row[label_col] not in (None, [], ""):
                    val = row[label_col]
                    st.write(f"**{code}**: {', '.join(val) if isinstance(val, list) else val}")

    # Location map
    lat, lon = row.get("_geopoint_latitude"), row.get("_geopoint_longitude")
    if pd.notna(lat) and pd.notna(lon):
        st.map(pd.DataFrame({"lat": [float(lat)], "lon": [float(lon)]}))
