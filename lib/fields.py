"""Resolve logical field -> Kobo question name by stable choice-list name.
Mirror of store_master/fields.py (this app is a separate deploy repo)."""

LIST_FIELDS = {
    "biz_type": "biz_type", "shop_name": "shop_name", "acquirer": "acquirer",
    "use_domestic": "YN_Use", "interested": "int", "qr": "QR",
    "payment": "Payment", "network": "Network", "why": "why", "revenue": "profit",
}
REQUIRED = {"biz_type", "shop_name", "acquirer", "use_domestic", "interested"}
# 2026-07 form inserts a `select_one License` question at S3.1_Q1, pushing these
# five detail text fields down by one (district S3.1_Q1 -> S3.1_Q2, ... phone
# S3.1_Q5 -> S3.1_Q6). Mirror of store_master/fields.py.
TEXT_FIELDS = {"district": "S3.1_Q2", "village": "S3.1_Q3",
               "owner_name": "S3.1_Q4", "nationality": "S3.1_Q5", "phone": "S3.1_Q6"}


def _survey(form):
    return (form.get("content") or {}).get("survey") or []


def _qname(q):
    return q.get("name") or q.get("$autoname")


def _qlist(q):
    ln = q.get("select_from_list_name")
    if ln:
        return ln
    t = str(q.get("type", ""))
    if t.startswith(("select_one ", "select_multiple ")):
        return t.split(" ", 1)[1]
    return None


def resolve_fields(form):
    survey = _survey(form)
    out = {}
    for logical, list_name in LIST_FIELDS.items():
        hits = [_qname(q) for q in survey if _qlist(q) == list_name and _qname(q)]
        if len(hits) == 1:
            out[logical] = hits[0]
        elif logical in REQUIRED:
            raise ValueError(f"field '{logical}': expected 1 question with list "
                             f"'{list_name}', found {len(hits)}: {hits}")
        else:
            out[logical] = None
    out["awareness"] = [_qname(q) for q in survey if _qlist(q) == "learn" and _qname(q)]
    out["psp"] = [_qname(q) for q in survey if _qlist(q) == "psp" and _qname(q)]
    names = {_qname(q) for q in survey}
    for logical, qn in TEXT_FIELDS.items():
        out[logical] = qn if qn in names else None
    return out
