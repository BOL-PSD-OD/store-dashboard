"""Thin KoboToolbox API layer: config + HTTP fetch (no Streamlit imports)."""
from __future__ import annotations
from dataclasses import dataclass
import requests

DEFAULT_SERVER = "https://kf.kobotoolbox.org"


@dataclass
class KoboConfig:
    token: str
    uid: str
    server: str = DEFAULT_SERVER

    @classmethod
    def from_mapping(cls, m) -> "KoboConfig":
        return cls(
            token=str(m.get("KOBO_TOKEN", "")),
            uid=str(m.get("KOBO_ASSET_UID", "")),
            server=str(m.get("KOBO_SERVER") or DEFAULT_SERVER).rstrip("/"),
        )


def _get_json(url: str, token: str) -> dict:
    resp = requests.get(url, headers={"Authorization": f"Token {token}"}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_form(cfg: KoboConfig) -> dict:
    return _get_json(f"{cfg.server}/api/v2/assets/{cfg.uid}.json", cfg.token)


def fetch_submissions(cfg: KoboConfig) -> list[dict]:
    url = f"{cfg.server}/api/v2/assets/{cfg.uid}/data.json?limit=10000"
    out: list[dict] = []
    while url:
        page = _get_json(url, cfg.token)
        out.extend(page.get("results", []))
        url = page.get("next")
    return out
