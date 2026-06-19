from streamlit.testing.v1 import AppTest


def test_map_page_renders():
    at = AppTest.from_file("pages/map.py")
    at.session_state["authenticated"] = True
    at.session_state["lang"] = "lo"
    at.run()
    assert not at.exception
    assert len(at.title) >= 1  # page title rendered (link_button + iframe are not introspectable)
