"""Pure transforms: Kobo form definition + submissions -> labelled DataFrame."""
from __future__ import annotations


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
        out.setdefault(c["list_name"], {})[str(c["name"])] = label_text(c.get("label"))
    return out


def build_question_meta(form: dict) -> dict[str, dict]:
    """{name: {'select': 'one'|'multiple'|None, 'list': list_name|None, 'label': str}}."""
    out: dict[str, dict] = {}
    for q in form.get("content", {}).get("survey", []):
        name = q.get("name")
        qtype = str(q.get("type", ""))
        if not name or qtype.startswith(("begin_", "end_")):
            continue
        select = None
        list_name = None
        if qtype.startswith("select_one"):
            select, list_name = "one", qtype.split(" ", 1)[1] if " " in qtype else None
        elif qtype.startswith("select_multiple"):
            select, list_name = "multiple", qtype.split(" ", 1)[1] if " " in qtype else None
        out[name] = {"select": select, "list": list_name, "label": label_text(q.get("label"))}
    return out
