"""Compare page: BOL survey (round 1) vs PSP follow-up (round 2) + conversion KPIs."""
import streamlit as st
from lib import data, charts, i18n, psp

BENTO_CSS = """
<style>
div[data-testid="stVerticalBlockBorderWrapper"]{
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 0.55rem 1rem 0.75rem;
}
div[data-testid="stMetric"]{ text-align: center; }
div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"]{ justify-content: center; }
</style>
"""

lang = st.session_state.get("lang", i18n.DEFAULT_LANG)
df = data.load_data()
pdf = data.load_psp_data()

st.title(i18n.t("compare_title", lang))
st.markdown(BENTO_CSS, unsafe_allow_html=True)

# --- Top KPI strip (before -> after + 2 conversion rates) ---
k = psp.kpis(df, pdf)
kpi_cards = [
    ("kpi_surveyed", str(k["surveyed"])),
    ("kpi_interested", str(k["interested"])),
    ("kpi_followed", str(k["followed_up"])),
    ("kpi_opened", str(k["opened"])),
    ("kpi_conv_followed", f'{k["conv_followed"]:.0f}%'),
    ("kpi_conv_overall", f'{k["conv_overall"]:.0f}%'),
]
for col, (key, val) in zip(st.columns(6), kpi_cards):
    with col.container(border=True):
        st.metric(i18n.t(key, lang), val)

st.divider()
left, right = st.columns(2)

# --- LEFT: BOL survey (round 1) ---
with left:
    st.subheader(i18n.t("compare_left", lang))
    with st.container(border=True):
        st.plotly_chart(charts.pie(psp.interest_series(df), i18n.t("chart_interest", lang)),
                        use_container_width=True)
    with st.container(border=True):
        st.plotly_chart(charts.pie(charts.count_by(df, "S3_Q1_label"), i18n.t("chart_biztype", lang)),
                        use_container_width=True)

# --- RIGHT: PSP follow-up (round 2) ---
with right:
    st.subheader(i18n.t("compare_right", lang))
    if pdf.empty:
        st.info(i18n.t("psp_no_data", lang))
    else:
        with st.container(border=True):
            st.plotly_chart(charts.pie(psp.result_series(pdf), i18n.t("chart_result", lang)),
                            use_container_width=True)
        with st.container(border=True):
            st.plotly_chart(charts.grouped_bar(psp.by_bank(pdf), i18n.t("chart_by_bank", lang)),
                            use_container_width=True)
