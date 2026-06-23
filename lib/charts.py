"""Pure aggregation helpers + Plotly figure builders (dark-theme friendly)."""
from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Qualitative palette that reads well on a dark background.
PALETTE = px.colors.qualitative.Set2
# Latin/digits -> Times New Roman, Lao -> Phetsarath (loaded app-wide via @import).
FONT_STACK = "'Times New Roman', 'Phetsarath', serif"


def _style(fig: go.Figure) -> go.Figure:
    """Transparent backgrounds + light font so charts blend into dark theme."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6e6e6", family=FONT_STACK),
        title=dict(font=dict(color="#fafafa", family=FONT_STACK)),
        legend=dict(font=dict(color="#e6e6e6")),
        margin=dict(t=55, b=20, l=10, r=10),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.12)", zerolinecolor="rgba(255,255,255,0.2)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.12)", zerolinecolor="rgba(255,255,255,0.2)")
    return fig


def count_by(df: pd.DataFrame, label_col: str) -> pd.Series:
    if label_col not in df.columns or df.empty:
        return pd.Series(dtype=int)
    return df[label_col].dropna().value_counts()


def count_multi(df: pd.DataFrame, label_list_col: str) -> pd.Series:
    if label_list_col not in df.columns or df.empty:
        return pd.Series(dtype=int)
    exploded = df[label_list_col].explode().dropna()
    return exploded.value_counts()


def count_multi_grouped(df: pd.DataFrame, col_to_context: dict) -> pd.DataFrame:
    """Count a provider list-column per context -> long DF [provider, context, count].

    col_to_context maps each ``*_label`` column to its context label, e.g.
    {"S3_Q10_label": "Lao QR", "S3_Q11_label": "Merchant QR", ...}.
    """
    rows = []
    for col, ctx in col_to_context.items():
        if col not in df.columns or df.empty:
            continue
        for provider, n in df[col].explode().dropna().value_counts().items():
            rows.append({"provider": provider, "context": ctx, "count": int(n)})
    return pd.DataFrame(rows, columns=["provider", "context", "count"])


def daily_counts(df: pd.DataFrame) -> pd.Series:
    if "_date" not in df.columns or df.empty:
        return pd.Series(dtype=int)
    return df["_date"].dropna().value_counts().sort_index()


def _date_key(s):
    """Sort key for 'DD/MM/YYYY' labels; non-dates (e.g. 'ອື່ນໆ') sort last."""
    try:
        d, m, y = str(s).split("/")
        return (0, int(y), int(m), int(d))
    except Exception:
        return (1, 0, 0, 0)


def interview_date_counts(df: pd.DataFrame, label_col: str = "_idate_label") -> pd.Series:
    """Forms per interview date (S0_Q1, formatted DD/MM/YYYY), chronological.

    Falls back to submission date (_date) if the interview-date column is absent.
    """
    if label_col not in df.columns or df[label_col].dropna().empty:
        return daily_counts(df)
    counts = df[label_col].dropna().value_counts()
    return counts.reindex(sorted(counts.index, key=_date_key))


def awareness_counts(df: pd.DataFrame, q_cols: list[str]) -> pd.DataFrame:
    rows = {}
    for q in q_cols:
        aware = not_aware = 0
        if q in df.columns:
            aware = int((df[q] == "1").sum())
            not_aware = int((df[q] == "0").sum())
        rows[q] = {"aware": aware, "not_aware": not_aware}
    return pd.DataFrame.from_dict(rows, orient="index")


def pie(series: pd.Series, title: str) -> go.Figure:
    if series.empty:
        return _style(go.Figure().update_layout(title=title, annotations=[
            dict(text="—", showarrow=False, font=dict(size=28, color="#888"))]))
    fig = px.pie(names=series.index, values=series.values, title=title, hole=0.4,
                 color_discrete_sequence=PALETTE)
    fig.update_traces(textinfo="value+percent")
    return _style(fig)


def bar(series: pd.Series, title: str) -> go.Figure:
    if series.empty:
        return _style(go.Figure().update_layout(title=title))
    data = pd.DataFrame({"cat": list(series.index), "val": list(series.values)})
    fig = px.bar(data, x="cat", y="val", title=title, text="val",
                 color="cat", color_discrete_sequence=PALETTE)
    fig.update_layout(xaxis_title="", yaxis_title="", legend_title_text="")
    return _style(fig)


def grouped_bar(long_df: pd.DataFrame, title: str) -> go.Figure:
    """Grouped bar from a long DF [provider, context, count] (see count_multi_grouped)."""
    if long_df.empty:
        return _style(go.Figure().update_layout(title=title, annotations=[
            dict(text="—", showarrow=False, font=dict(size=28, color="#888"))]))
    fig = px.bar(long_df, x="provider", y="count", color="context", barmode="group",
                 title=title, text="count", color_discrete_sequence=PALETTE)
    fig.update_layout(xaxis_title="", yaxis_title="", legend_title_text="")
    return _style(fig)


def daily_bar(series: pd.Series, title: str) -> go.Figure:
    if series.empty:
        return _style(go.Figure().update_layout(title=title))
    fig = px.bar(x=[str(d) for d in series.index], y=series.values, title=title,
                 text=series.values, color_discrete_sequence=["#4dabf7"])
    fig.update_layout(xaxis_title="", yaxis_title="")
    return _style(fig)


def awareness_hbar(table: pd.DataFrame, labels: dict, aware_txt: str,
                   not_aware_txt: str, title: str) -> go.Figure:
    """table indexed by question code with columns aware/not_aware;
    labels maps code -> display question text."""
    fig = go.Figure()
    if table.empty:
        return _style(fig.update_layout(title=title))
    y = [labels.get(q, q) for q in table.index]
    fig.add_bar(y=y, x=table["aware"], name=aware_txt, orientation="h",
                marker_color="#2f9e44", text=table["aware"])
    fig.add_bar(y=y, x=table["not_aware"], name=not_aware_txt, orientation="h",
                marker_color="#e03131", text=table["not_aware"])
    fig.update_layout(barmode="stack", title=title, xaxis_title="", yaxis_title="")
    fig.update_yaxes(autorange="reversed")  # 3.1 at top, 3.5 at bottom
    return _style(fig)
