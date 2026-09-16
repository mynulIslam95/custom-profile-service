#!/usr/bin/env python3
"""Smoke check after a deploy.

Hit health/ready, create one draft profile, then drop it from the
in-memory store by process restart (no delete API on purpose).

Used from CI after the image is built, or locally against uvicorn.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def get_json(url: str) -> tuple[int, dict]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        return exc.code, {}


def post_json(url: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, method="POST", headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    code, health = get_json(base + "/health")
    if code != 200 or health.get("status") != "ok":
        print("health failed", code, health)
        return 1
    print("health ok, version", health.get("version"))

    code, ready = get_json(base + "/ready")
    if code != 200:
        print("ready failed", code)
        return 1

    code, created = post_json(
        base + "/profiles",
        {
            "product_sku": "SMOKE-1",
            "customer_ref": "ci",
            "feature_set": "smoke",
        },
    )
    if code != 201:
        print("create failed", code, created)
        return 1
    print("created", created.get("id"), created.get("status"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
