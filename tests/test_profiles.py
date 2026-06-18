from streamlit.testing.v1 import AppTest
from lib import decode

def _authed_profiles(monkeypatch, form, subs):
    import lib.data as data
    df = decode.decode_submissions(subs, form)
    monkeypatch.setattr(data, "load_data", lambda: df)  # auto-restored after test
    at = AppTest.from_file("pages/store_profiles.py")
    at.session_state["authenticated"] = True
    at.session_state["lang"] = "lo"
    return at.run()

def test_profiles_renders(monkeypatch, form, subs):
    at = _authed_profiles(monkeypatch, form, subs)
    assert not at.exception
    assert len(at.selectbox) >= 1  # store-type filter present

def test_profiles_handles_empty(monkeypatch, form):
    at = _authed_profiles(monkeypatch, form, [])
    assert not at.exception
