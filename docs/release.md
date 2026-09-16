# How I cut a lab release

1. Tests have to be green (`pytest -q`).
2. Version is `APP_VERSION` in `src/app.py`. Bump it when the behaviour changes.
3. `docker build -t custom-profile-service:1.2.0 .`
4. Apply k8s manifests on the local cluster (`kind` on my machine):
   - `kubectl apply -f k8s/`
5. `python scripts/smoke_check.py --base http://127.0.0.1:8000`

If smoke fails I do not mark the version as released.

Jenkinsfile covers the same test + package steps for a Jenkins agent.
GitHub Actions is what actually runs on every push here.

No production cluster in this repo. Image tag is local / CI only.
