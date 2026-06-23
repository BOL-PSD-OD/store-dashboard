import datetime as dt
import plotly.graph_objects as go
from lib import charts, decode

def test_count_by(form, subs):
    df = decode.decode_submissions(subs, form)
    counts = charts.count_by(df, "S3_Q1_label")
    assert counts["ຮ້ານອາຫານ"] == 1
    assert counts["ໂຮງແຮມ"] == 1

def test_count_multi(form, subs):
    df = decode.decode_submissions(subs, form)
    counts = charts.count_multi(df, "_psp_label")
    assert counts["BCEL"] == 2
    assert counts["JDB"] == 1

def test_status_pie_series(form, subs):
    df = decode.decode_submissions(subs, form)
    counts = charts.count_by(df, "_status_label")
    assert counts[decode.STATUS_LABELS["both_int"]] == 1
    assert counts[decode.STATUS_LABELS["foreign_unint"]] == 1

def test_daily_counts(form, subs):
    df = decode.decode_submissions(subs, form)
    daily = charts.daily_counts(df)
    assert daily[dt.date(2026, 6, 29)] == 2

def test_awareness_counts(form, subs):
    df = decode.decode_submissions(subs, form)
    table = charts.awareness_counts(df, ["S4_Q1"])
    assert table.loc["S4_Q1", "aware"] == 1
    assert table.loc["S4_Q1", "not_aware"] == 1

def test_pie_returns_figure(form, subs):
    df = decode.decode_submissions(subs, form)
    fig = charts.pie(charts.count_by(df, "S3_Q1_label"), "title")
    assert isinstance(fig, go.Figure)

def test_pie_empty_returns_figure():
    import pandas as pd
    fig = charts.pie(pd.Series(dtype=int), "title")
    assert isinstance(fig, go.Figure)
