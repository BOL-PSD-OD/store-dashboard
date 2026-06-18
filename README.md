# store-dashboard — Luang Prabang store survey dashboard

Password-gated Streamlit app reading live from KoboToolbox. Two pages:
**Dashboard** (KPIs + charts) and **Store Profiles** (filter / search / profile).

## Local run

```bash
# Python 3.12 recommended. With uv installed:
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements-dev.txt

# add local secrets (gitignored):
cp secrets.example.toml .streamlit/secrets.toml   # then edit real values

.venv/Scripts/streamlit run streamlit_app.py
```

## Tests

```bash
.venv/Scripts/python -m pytest -q
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a new GitHub repo.
2. https://share.streamlit.io -> **New app** -> pick repo / branch / `streamlit_app.py`.
3. **Advanced settings -> Python 3.12**.
4. Paste **Secrets** (TOML):

   ```toml
   APP_PASSWORD   = "..."
   KOBO_TOKEN     = "..."
   KOBO_ASSET_UID = "..."
   KOBO_SERVER    = "https://kf.kobotoolbox.org"
   ```
5. Deploy. App auto-redeploys on every push.

> The Kobo token stays server-side (never reaches the browser). The whole app is gated by `APP_PASSWORD`.

## How it works

- `lib/kobo.py` — fetches submissions + form definition from the Kobo API (token from `st.secrets`).
- `lib/decode.py` — turns coded answers into a labelled DataFrame (handles select_multiple, group prefixes, local dates).
- `lib/data.py` — cached `load_data()` (5-min TTL) joining fetch + decode; sidebar **Refresh** clears it.
- `lib/charts.py` — pure aggregation + Plotly figure builders.
- `lib/i18n.py` — Lao/English UI strings + a language toggle.
- `lib/auth.py` — single shared-password gate with 30-min idle timeout.
- `streamlit_app.py` — auth gate via `st.navigation`; authenticated users get Dashboard + Store Profiles.
