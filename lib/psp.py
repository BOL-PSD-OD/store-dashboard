"""PSP follow-up (round 2) data + pure aggregations for the compare page.
Pure helpers take DataFrames so they unit-test offline; fetch_psp does I/O."""
from __future__ import annotations
import pandas as pd

# 9-state status key -> short interest bucket (mirrors kobo_sync/psp_export._INTEREST).
INTEREST_SHORT = {
    "both_int": "ສົນໃຈ", "foreign_int": "ສົນໃຈ", "notool_int": "ສົນໃຈ",
    "both_unint": "ບໍ່ສົນໃຈ", "foreign_unint": "ບໍ່ສົນໃຈ", "notool_unint": "ບໍ່ສົນໃຈ",
    "both_using": "ໃຊ້ແລ້ວ", "foreign_using": "ໃຊ້ແລ້ວ", "domestic": "ໃຊ້ແລ້ວ",
}
INTERESTED_KEYS = ("both_int", "foreign_int", "notool_int")
OPENED = "ເປີດ"          # last_result value when an account was opened


def psp_dataframe(rows) -> pd.DataFrame:
    """Round-2 sheet rows (list of dicts from gspread) -> DataFrame."""
    return pd.DataFrame(rows)


def interest_series(round1_df: pd.DataFrame) -> pd.Series:
    """Count round-1 stores by short interest bucket (from derived _status)."""
    if "_status" not in round1_df.columns or round1_df.empty:
        return pd.Series(dtype=int)
    buckets = round1_df["_status"].map(lambda k: INTEREST_SHORT.get(k, "ບໍ່ລະບຸ"))
    return buckets.value_counts()


def _last_result(pdf: pd.DataFrame) -> pd.Series:
    if "last_result" not in pdf.columns or pdf.empty:
        return pd.Series(dtype=object)
    return pdf["last_result"].fillna("").astype(str).str.strip()


def result_series(pdf: pd.DataFrame) -> pd.Series:
    lr = _last_result(pdf)
    if lr.empty:
        return pd.Series(dtype=int)

    def bucket(v):
        if v == OPENED:
            return "🟢 ເປີດ"
        if v == "ບໍ່ເປີດ":
            return "🔵 ໄປແລ້ວ·ບໍ່ເປີດ"
        return "⚪ ຍັງບໍ່ໄປ"

    return lr.map(bucket).value_counts()


def by_bank(pdf: pd.DataFrame) -> pd.DataFrame:
    """Long DF [provider, context, count] for charts.grouped_bar:
    provider = PSP bank; context = 'ເປີດ' (opened) vs 'ຍັງ' (not yet)."""
    cols = ["provider", "context", "count"]
    if pdf.empty or "PSP" not in pdf.columns:
        return pd.DataFrame(columns=cols)
    work = pd.DataFrame({"provider": pdf["PSP"].fillna("").astype(str),
                         "opened": _last_result(pdf).eq(OPENED)})
    work = work[work["provider"] != ""]
    rows = []
    for bank, grp in work.groupby("provider"):
        opened = int(grp["opened"].sum())
        rows.append({"provider": bank, "context": "ເປີດ", "count": opened})
        rows.append({"provider": bank, "context": "ຍັງ", "count": int(len(grp) - opened)})
    return pd.DataFrame(rows, columns=cols)


def _pct(num: int, den: int) -> float:
    return round(num / den * 100.0, 1) if den else 0.0


def kpis(round1_df: pd.DataFrame, pdf: pd.DataFrame) -> dict:
    surveyed = int(len(round1_df))
    if "_status" in round1_df.columns and not round1_df.empty:
        interested = int(round1_df["_status"].isin(INTERESTED_KEYS).sum())
    else:
        interested = 0
    lr = _last_result(pdf)
    followed_up = int((lr != "").sum()) if not lr.empty else 0
    opened = int(lr.eq(OPENED).sum()) if not lr.empty else 0
    return {
        "surveyed": surveyed, "interested": interested,
        "followed_up": followed_up, "opened": opened,
        "conv_followed": _pct(opened, followed_up),
        "conv_overall": _pct(opened, interested),
    }
