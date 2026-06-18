from streamlit.testing.v1 import AppTest


def test_map_page_renders():
    at = AppTest.from_file("pages/map.py")
    at.session_state["authenticated"] = True
    at.session_state["lang"] = "lo"
    at.run()
    assert not at.exception
    # the "open in new tab" link should be present in the rendered markdown
    assert any("panngeun.github.io/kobo-live-map" in str(m.value) for m in at.markdown)
