"""Pure transforms: Kobo form definition + submissions -> labelled DataFrame."""
from __future__ import annotations

import datetime as dt
import pandas as pd
from lib.fields import resolve_fields


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


def _ddmmyyyy(iso: str):
    """ISO date / datetime -> 'DD/MM/YYYY' (used for the interview date S0_Q1)."""
    d = _to_local_date(iso)
    return d.strftime("%d/%m/%Y") if d else None


# --- Derived account status (9 states) --------------------------------------
# Mirrors kobo-live-map/build_map.py and store_master/status.py. Status is
# S3_Q7 (acquirer) x S3_Q12 (use_domestic) x S3_Q15 (interested). S3_Q7 codes:
# "1" domestic, "2"/"0" foreign ("0" = legacy form), "3" no payment tool.
STATUS_LABELS = {  # key -> Lao label for pie slices / profile / table
    "domestic":      "ໃນ · ມີ QR",
    "both_using":    "ໃນ+ນອກ · ໃຊ້ພາຍໃນ",
    "foreign_using": "ນອກ · ໃຊ້ພາຍໃນ",
    "both_int":      "ໃນ+ນອກ · ບໍ່ໃຊ້ · ສົນໃຈ",
    "foreign_int":   "ນອກ · ບໍ່ໃຊ້ · ສົນໃຈ",
    "notool_int":    "ບໍ່ມີເຄື່ອງມື · ສົນໃຈ",
    "both_unint":    "ໃນ+ນອກ · ບໍ່ໃຊ້ · ບໍ່ສົນໃຈ",
    "foreign_unint": "ນອກ · ບໍ່ໃຊ້ · ບໍ່ສົນໃຈ",
    "notool_unint":  "ບໍ່ມີເຄື່ອງມື · ບໍ່ສົນໃຈ",
    "unknown":       "ບໍ່ລະບຸ",
}
IN_SYSTEM = ("domestic", "both_using", "foreign_using")  # KPI "success" group


def derive_status(acquirer, use_domestic, interested) -> str:
    """acquirer: iterable of S3_Q7 codes; use_domestic/interested: '1'/'0'/None."""
    acq = set(acquirer or [])
    dom = "1" in acq
    foreign = "2" in acq or "0" in acq
    notool = "3" in acq
    if dom and foreign:
        if use_domestic == "1":
            return "both_using"
        return "both_int" if interested == "1" else "both_unint"
    if foreign:
        if use_domestic == "1":
            return "foreign_using"
        return "foreign_int" if interested == "1" else "foreign_unint"
    if dom:
        return "domestic"
    if notool:
        return "notool_int" if interested == "1" else "notool_unint"
    return "unknown"


# Derived columns added to every decoded row (also seeded on the empty frame).
DERIVED_COLS = ["_date", "_idate_label", "_status", "_status_label", "_psp_label"]

# Fallback field map (new-form numbers) when a form is too partial to resolve
# (keeps this read-only viewer from crashing; the engine stays strictly fail-loud).
_FALLBACK_FIELDS = {"acquirer": "S3_Q4", "use_domestic": "S3_Q9",
                    "interested": "S3_Q12", "psp": []}


def _enrich(row: dict, flat: dict, fields: dict) -> None:
    """Add the derived columns (status, interview date, combined PSP) using the
    resolved field map (resilient to question renumbering)."""
    row["_date"] = _to_local_date(flat.get("_submission_time"))
    row["_idate_label"] = _ddmmyyyy(flat.get("S0_Q1"))
    acq_col = fields.get("acquirer")
    acq = row.get(acq_col) if isinstance(row.get(acq_col), list) else []
    status = derive_status(acq, row.get(fields.get("use_domestic")), row.get(fields.get("interested")))
    row["_status"] = status
    row["_status_label"] = STATUS_LABELS.get(status, status)
    psp: list[str] = []
    for q in fields.get("psp", []):
        for x in (row.get(q + "_label") or []):
            if x and x not in psp:
                psp.append(x)
    row["_psp_label"] = psp


def decode_submissions(subs: list[dict], form: dict) -> pd.DataFrame:
    qmeta = build_question_meta(form)
    cmap = build_choice_map(form)
    try:
        fields = resolve_fields(form)
    except ValueError:
        fields = dict(_FALLBACK_FIELDS)
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
        _enrich(row, flat, fields)
        rows.append(row)

    if not rows:
        cols = []
        for name, meta in qmeta.items():
            cols.append(name)
            if meta["select"]:
                cols.append(name + "_label")
        cols += DERIVED_COLS
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(rows)
