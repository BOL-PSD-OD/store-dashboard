from streamlit.testing.v1 import AppTest

def _run():
    at = AppTest.from_file("streamlit_app.py")
    at.secrets["APP_PASSWORD"] = "pw"
    at.secrets["KOBO_TOKEN"] = "t"
    at.secrets["KOBO_ASSET_UID"] = "u"
    return at.run()

def test_unauthenticated_shows_login():
    at = _run()
    assert not at.exception
    assert len(at.text_input) >= 1  # password field present

def test_wrong_password_shows_error():
    at = _run()
    at.text_input[0].set_value("wrong").run()
    at.button[0].click().run()
    assert len(at.error) >= 1
