"""Dashboard page: KPI cards, daily chart, pies, awareness, PSP bar."""
import datetime as dt
import streamlit as st
from lib import data, charts, i18n

lang = st.session_state.get("lang", i18n.DEFAULT_LANG)
df = data.load_data()

st.title(i18n.t("dashboard_title", lang))

if df.empty:
    st.info(i18n.t("no_data", lang))
    st.metric(i18n.t("kpi_total", lang), 0)
    st.metric(i18n.t("kpi_today", lang), 0)
    st.metric(i18n.t("kpi_days", lang), 0)
    st.metric(i18n.t("kpi_districts", lang), 0)
    st.stop()

# --- KPI cards (interview date = S1_Q5, falls back to submission date) ---
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

c1, c2, c3, c4 = st.columns(4)
c1.metric(i18n.t("kpi_total", lang), total)
c2.metric(i18n.t("kpi_today", lang), today_n)
c3.metric(i18n.t("kpi_days", lang), days)
c4.metric(i18n.t("kpi_districts", lang), districts)

# --- Daily chart (by interview date S1_Q5) ---
st.plotly_chart(charts.daily_bar(charts.interview_date_counts(df), i18n.t("chart_daily", lang)),
                use_container_width=True)

# --- 6 pies in a 3x2 grid ---
pie_specs = [
    ("S2_Q1_label", "chart_biztype"),
    ("S2_Q3_label", "chart_license"),
    ("S2_Q7_label", "chart_status"),
    ("S2_Q4_label", "chart_market"),
    ("S2_Q5_label", "chart_qr"),
    ("S2_Q11_label", "chart_night"),
]
cols = st.columns(3)
for i, (col, key) in enumerate(pie_specs):
    fig = charts.pie(charts.count_by(df, col), i18n.t(key, lang))
    cols[i % 3].plotly_chart(fig, use_container_width=True)

# --- Section-3 awareness (stacked horizontal bar) ---
s3 = [c for c in ["S3_Q1", "S3_Q2", "S3_Q3", "S3_Q4", "S3_Q5"] if c in df.columns]
labels = {q: f"{q[1]}.{q[-1]}" for q in s3}  # 'S3_Q1' -> '3.1'
st.plotly_chart(
    charts.awareness_hbar(charts.awareness_counts(df, s3), labels,
                          i18n.t("aware_yes", lang), i18n.t("aware_no", lang),
                          i18n.t("chart_awareness", lang)),
    use_container_width=True)

# --- PSP bar (select_multiple) ---
st.plotly_chart(charts.bar(charts.count_multi(df, "S2_Q8_label"), i18n.t("chart_psp", lang)),
                use_container_width=True)
