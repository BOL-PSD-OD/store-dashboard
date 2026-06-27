"""Dashboard page: KPI cards, daily chart, pies, awareness, PSP bar (bento layout)."""
import datetime as dt
import streamlit as st
from lib import data, charts, i18n

# Bento cards: round + tint every bordered container; center the KPI metrics.
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

st.title(i18n.t("dashboard_title", lang))
st.markdown(BENTO_CSS, unsafe_allow_html=True)

if df.empty:
    st.info(i18n.t("no_data", lang))
    for k in ("kpi_total", "kpi_today", "kpi_days", "kpi_districts", "kpi_villages"):
        st.metric(i18n.t(k, lang), 0)
    st.stop()

# --- KPI values (interview date = S0_Q1, falls back to submission date) ---
today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=7)).date()
today_str = today.strftime("%d/%m/%Y")
date_col = "_idate_label" if "_idate_label" in df.columns and df["_idate_label"].notna().any() else None

total = len(df)
if date_col:
    today_n = int((df[date_col] == today_str).sum())
    days = int(df[date_col].dropna().nunique())
else:
    today_n = int((df["_date"] == today).sum()) if "_date" in df.columns else 0
    days = int(df["_date"].dropna().nunique()) if "_date" in df.columns else 0
districts = int(df["S3.1_Q1"].dropna().nunique()) if "S3.1_Q1" in df.columns else 0
villages = int(df["S3.1_Q2"].dropna().nunique()) if "S3.1_Q2" in df.columns else 0

# --- KPI cards (each its own bento cell) ---
kpis = [("kpi_total", total), ("kpi_today", today_n), ("kpi_days", days),
        ("kpi_districts", districts), ("kpi_villages", villages)]
for col, (key, val) in zip(st.columns(5), kpis):
    with col.container(border=True):
        st.metric(i18n.t(key, lang), val)

# --- Daily chart (by interview date S1_Q5) ---
with st.container(border=True):
    st.plotly_chart(charts.daily_bar(charts.interview_date_counts(df), i18n.t("chart_daily", lang)),
                    use_container_width=True)

# --- 6 pies in a 3x2 grid, each in its own bento card ---
# (col, i18n key, is multi-select?). Account status is the derived 9-state column.
pie_specs = [
    ("S3_Q1_label", "chart_biztype", False), ("S3_Q14_label", "chart_revenue", False),
    ("S3_Q12_label", "chart_interested", False),
    ("S3_Q6_label", "chart_qr", True), ("S3_Q11_label", "chart_network", True),
    ("S3.1_Q4", "chart_nationality", False),   # owner nationality (free text)
]
cols = st.columns(3)
for i, (col, key, multi) in enumerate(pie_specs):
    series = charts.count_multi(df, col) if multi else charts.count_by(df, col)
    with cols[i % 3].container(border=True):
        st.plotly_chart(charts.pie(series, i18n.t(key, lang)), use_container_width=True)

# --- Section-4 awareness + full question list (one bento card) ---
s2 = [c for c in ["S2_Q1", "S2_Q2", "S2_Q3"] if c in df.columns]
labels = {q: f"{q[1]}.{q.split('_Q')[-1]}" for q in s2}  # 'S2_Q1' -> '2.1'
qlabels = data.load_question_labels()
with st.container(border=True):
    st.plotly_chart(
        charts.awareness_hbar(charts.awareness_counts(df, s2), labels,
                              i18n.t("aware_yes", lang), i18n.t("aware_no", lang),
                              i18n.t("chart_awareness", lang)),
        use_container_width=True)
    if s2:
        st.markdown(f"**{i18n.t('section4_questions', lang)}**")
        for q in s2:
            # form label already starts with the '4.x' number, so show it as-is
            st.markdown(f"- {qlabels.get(q, q)}")

# --- PSP grouped bar (bento card) — split by the 3 contexts ---
# S3_Q10 = Lao QR, S3_Q11 = merchant QR, S3_Q13 = foreign acceptance.
psp_ctx = {
    "S3_Q7_label":  i18n.t("psp_ctx_laoqr", lang),
    "S3_Q8_label":  i18n.t("psp_ctx_merchant", lang),
    "S3_Q10_label": i18n.t("psp_ctx_foreign", lang),
}
with st.container(border=True):
    st.plotly_chart(
        charts.grouped_bar(charts.count_multi_grouped(df, psp_ctx), i18n.t("chart_psp", lang)),
        use_container_width=True)
