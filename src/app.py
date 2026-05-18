"""Demo service for product customization profiles.

Used to practice testing a new version before it is marked released.
In-memory store only — nothing is persisted.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_VERSION = "1.2.0"

app = FastAPI(title="Custom Profile Service", version=APP_VERSION)

_STORE: Dict[str, "Profile"] = {}
_READY = True


class ProfileIn(BaseModel):
    product_sku: str = Field(min_length=3, max_length=32)
    customer_ref: str = Field(min_length=1, max_length=64)
    feature_set: str = Field(min_length=1)
    note: Optional[str] = None


class Profile(ProfileIn):
    id: str
    status: str


def reset_store() -> None:
    _STORE.clear()


def set_ready(flag: bool) -> None:
    global _READY
    _READY = flag


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": APP_VERSION}


@app.get("/ready")
def ready() -> dict:
    if not _READY:
        raise HTTPException(status_code=503, detail="not ready")
    return {"ready": True, "version": APP_VERSION}


@app.post("/profiles", response_model=Profile, status_code=201)
def create_profile(body: ProfileIn) -> Profile:
    if " " in body.product_sku:
        raise HTTPException(status_code=400, detail="sku must not contain spaces")
    profile = Profile(id=str(uuid4()), status="draft", **body.model_dump())
    _STORE[profile.id] = profile
    return profile


@app.get("/profiles", response_model=List[Profile])
def list_profiles(status: Optional[str] = None) -> List[Profile]:
    items = list(_STORE.values())
    if status:
        items = [p for p in items if p.status == status]
    return items


@app.get("/profiles/{pid}", response_model=Profile)
def get_profile(pid: str) -> Profile:
    profile = _STORE.get(pid)
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile


@app.post("/profiles/{pid}/release", response_model=Profile)
def release_profile(pid: str) -> Profile:
    profile = _STORE.get(pid)
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    if profile.status == "blocked":
        raise HTTPException(status_code=409, detail="blocked profile cannot be released")
    profile.status = "released"
    _STORE[pid] = profile
    return profile
