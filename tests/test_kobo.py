from lib import kobo

def test_kobo_config_from_mapping():
    cfg = kobo.KoboConfig.from_mapping({
        "KOBO_TOKEN": "tok", "KOBO_ASSET_UID": "uid",
        "KOBO_SERVER": "https://eu.kobotoolbox.org/",
    })
    assert cfg.token == "tok"
    assert cfg.uid == "uid"
    assert cfg.server == "https://eu.kobotoolbox.org"  # trailing slash stripped

def test_kobo_config_default_server():
    cfg = kobo.KoboConfig.from_mapping({"KOBO_TOKEN": "t", "KOBO_ASSET_UID": "u"})
    assert cfg.server == "https://kf.kobotoolbox.org"

def test_fetch_submissions_paginates(monkeypatch):
    cfg = kobo.KoboConfig(token="t", uid="u", server="https://k")
    pages = {
        "https://k/api/v2/assets/u/data.json?limit=10000":
            {"results": [{"_id": 1}], "next": "https://k/next"},
        "https://k/next": {"results": [{"_id": 2}], "next": None},
    }
    monkeypatch.setattr(kobo, "_get_json", lambda url, token: pages[url])
    out = kobo.fetch_submissions(cfg)
    assert [r["_id"] for r in out] == [1, 2]
