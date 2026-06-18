from lib import decode

def test_strip_group():
    assert decode.strip_group("Section_2/S2_Q1") == "S2_Q1"
    assert decode.strip_group("S1_Q1") == "S1_Q1"

def test_label_text_handles_list_and_string():
    assert decode.label_text(["ແມ່ນ"]) == "ແມ່ນ"
    assert decode.label_text("BCEL") == "BCEL"
    assert decode.label_text(None) == ""

def test_build_choice_map(form):
    cm = decode.build_choice_map(form)
    assert cm["YN"]["1"] == "ແມ່ນ"
    assert cm["psp"]["2"] == "JDB"

def test_build_question_meta(form):
    qm = decode.build_question_meta(form)
    assert qm["S2_Q1"] == {"select": "one", "list": "biz_type", "label": "2.1 biz type"}
    assert qm["S2_Q8"]["select"] == "multiple"
    assert "S1_Q1" in qm
    assert "Section_2" not in qm  # groups excluded
