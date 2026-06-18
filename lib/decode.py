"""Pure transforms: Kobo form definition + submissions -> labelled DataFrame."""
from __future__ import annotations

import datetime as dt
import pandas as pd


def strip_group(key: str) -> str:
    """'Section_2/S2_Q1' -> 'S2_Q1' (Kobo prefixes answers with group path)."""
    return key.split("/")[-1]


def label_text(val) -> str:
    """Kobo labels are a list (one per language) or a plain string."""
    if val is None:
        return ""
    if isinstance(val, list):
        return label_text(val[0]) if val else ""
    return str(val)


def build_choice_map(form: dict) -> dict[str, dict[str, str]]:
    """{list_name: {code: label}} from form['content']['choices']."""
    out: dict[str, dict[str, str]] = {}
    for c in form.get("content", {}).get("choices", []):
        ln = c.get("list_name")
        nm = c.get("name", c.get("$autovalue"))
        if ln is None or nm is None:
            continue
        out.setdefault(ln, {})[str(nm)] = label_text(c.get("label")) or str(nm)
    return out


def build_question_meta(form: dict) -> dict[str, dict]:
    """{name: {'select': 'one'|'multiple'|None, 'list': list_name|None, 'label': str}}.

    Handles both the Kobo asset-content shape (``type='select_one'`` plus a
    separate ``select_from_list_name`` key) and the XLSForm shape
    (``type='select_one biz_type'``).
    """
    out: dict[str, dict] = {}
    for q in form.get("content", {}).get("survey", []):
        name = q.get("name") or q.get("$autoname")
        qtype = str(q.get("type", ""))
        if not name or qtype.startswith(("begin_", "end_")):
            continue
        select = None
        if qtype.startswith("select_one"):
            select = "one"
        elif qtype.startswith("select_multiple"):
            select = "multiple"
        list_name = q.get("select_from_list_name")
        if select and not list_name and " " in qtype:
            list_name = qtype.split(" ", 1)[1]  # XLSForm combined-type fallback
        out[name] = {"select": select, "list": list_name, "label": label_text(q.get("label"))}
    return out


def build_question_labels(form: dict) -> dict[str, str]:
    """Ordered {name: label} for every named question that has a label.

    Group/section rows are skipped. Survey order is preserved so the profile
    page can render fields in the order they appear in the form, and it adapts
    automatically when the form gains/renames questions.
    """
    out: dict[str, str] = {}
    for q in form.get("content", {}).get("survey", []):
        name = q.get("name") or q.get("$autoname")
        qtype = str(q.get("type", ""))
        if not name or qtype.startswith(("begin_", "end_")):
            continue
        lab = label_text(q.get("label"))
        if lab:
            out[name] = lab
    return out


VIENTIANE_OFFSET = dt.timedelta(hours=7)


def _to_local_date(iso: str):
    if not iso:
        return None
    s = str(iso).replace("Z", "")
    try:
        ts = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    return (ts + VIENTIANE_OFFSET).date()


def decode_submissions(subs: list[dict], form: dict) -> pd.DataFrame:
    qmeta = build_question_meta(form)
    cmap = build_choice_map(form)
    rows = []
    for rec in subs:
        flat = {strip_group(k): v for k, v in rec.items()}
        row = dict(flat)
        for name, meta in qmeta.items():
            raw = flat.get(name)
            lst = cmap.get(meta["list"], {})
            if meta["select"] == "multiple":
                codes = str(raw).split() if raw not in (None, "") else []
                row[name] = codes
                row[name + "_label"] = [lst.get(c, c) for c in codes]
            elif meta["select"] == "one":
                code = "" if raw is None else str(raw)
                row[name] = code if code else None
                row[name + "_label"] = lst.get(code) if code else None
        row["_date"] = _to_local_date(flat.get("_submission_time"))
        rows.append(row)

    if not rows:
        cols = []
        for name, meta in qmeta.items():
            cols.append(name)
            if meta["select"]:
                cols.append(name + "_label")
        cols.append("_date")
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(rows)
