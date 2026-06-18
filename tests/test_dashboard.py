from streamlit.testing.v1 import AppTest
from lib import decode

def _authed_dashboard(monkeypatch, form, subs):
    import lib.data as data
    df = decode.decode_submissions(subs, form)
    monkeypatch.setattr(data, "load_data", lambda: df)  # auto-restored after test
    at = AppTest.from_file("pages/dashboard.py")
    at.session_state["authenticated"] = True
    at.session_state["lang"] = "lo"
    return at.run()

def test_dashboard_renders_kpis(monkeypatch, form, subs):
    at = _authed_dashboard(monkeypatch, form, subs)
    assert not at.exception
    assert len(at.metric) >= 4  # four KPI cards

def test_dashboard_handles_empty(monkeypatch, form):
    at = _authed_dashboard(monkeypatch, form, [])
    assert not at.exception
