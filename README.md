# custom-profile-service

Lab service for product customization profiles (draft → released).

I built this next to my studies to practice what a DevOps working student
does on an application: tests on every change, a container image,
a small Kubernetes deploy, and a smoke check after the new version is up.

Not connected to any company system. In-memory store.

## API

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health` | includes `version` |
| GET | `/ready` | 503 when not ready |
| POST | `/profiles` | create draft |
| GET | `/profiles` | optional `?status=` |
| GET | `/profiles/{id}` | |
| POST | `/profiles/{id}/release` | draft → released |

SKU cannot contain spaces. Blocked profiles cannot be released.

## Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn src.app:app --reload
python scripts/smoke_check.py
```

## Deploy bits

- `Dockerfile`
- `k8s/` — Deployment, Service, ConfigMap, probes. I ran this on `kind`.
- `.github/workflows/ci.yml` — pytest, then `docker build`
- `Jenkinsfile` — same test + package stages if the job runs on Jenkins

See `docs/release.md`.
