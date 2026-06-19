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

# --- KPI values (interview date = S1_Q5, falls back to submission date) ---
today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=7)).date()
today_str = today.strftime("%d/%m/%Y")
date_col = "S1_Q5_label" if "S1_Q5_label" in df.columns and df["S1_Q5_label"].notna().any() else None

total = len(df)
if date_col:
    today_n = int((df[date_col] == today_str).sum())
    days = int(df[date_col].dropna().nunique())
else:
    today_n = int((df["_date"] == today).sum()) if "_date" in df.columns else 0
    days = int(df["_date"].dropna().nunique()) if "_date" in df.columns else 0
districts = int(df["S2_Q9_label"].dropna().nunique()) if "S2_Q9_label" in df.columns else 0
villages = int(df["S2_Q10_label"].dropna().nunique()) if "S2_Q10_label" in df.columns else 0

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
pie_specs = [
    ("S2_Q1_label", "chart_biztype"), ("S2_Q3_label", "chart_license"),
    ("S2_Q7_label", "chart_status"), ("S2_Q4_label", "chart_market"),
    ("S2_Q5_label", "chart_qr"), ("S2_Q11_label", "chart_night"),
]
cols = st.columns(3)
for i, (col, key) in enumerate(pie_specs):
    with cols[i % 3].container(border=True):
        st.plotly_chart(charts.pie(charts.count_by(df, col), i18n.t(key, lang)),
                        use_container_width=True)

# --- Section-3 awareness + full question list (one bento card) ---
s3 = [c for c in ["S3_Q1", "S3_Q2", "S3_Q3", "S3_Q4", "S3_Q5"] if c in df.columns]
labels = {q: f"{q[1]}.{q[-1]}" for q in s3}  # 'S3_Q1' -> '3.1'
qlabels = data.load_question_labels()
with st.container(border=True):
    st.plotly_chart(
        charts.awareness_hbar(charts.awareness_counts(df, s3), labels,
                              i18n.t("aware_yes", lang), i18n.t("aware_no", lang),
                              i18n.t("chart_awareness", lang)),
        use_container_width=True)
    if s3:
        st.markdown(f"**{i18n.t('section3_questions', lang)}**")
        for q in s3:
            # form label already starts with the '3.x' number, so show it as-is
            st.markdown(f"- {qlabels.get(q, q)}")

# --- PSP bar (bento card) ---
with st.container(border=True):
    st.plotly_chart(charts.bar(charts.count_multi(df, "S2_Q8_label"), i18n.t("chart_psp", lang)),
                    use_container_width=True)
