def _payload(**extra):
    data = {
        "product_sku": "NFC-A12",
        "customer_ref": "cust-17",
        "feature_set": "pay,transit",
    }
    data.update(extra)
    return data


def test_create_and_get(client):
    r = client.post("/profiles", json=_payload())
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "draft"
    pid = body["id"]

    got = client.get(f"/profiles/{pid}")
    assert got.status_code == 200
    assert got.json()["product_sku"] == "NFC-A12"


def test_reject_sku_with_space(client):
    r = client.post("/profiles", json=_payload(product_sku="bad sku"))
    assert r.status_code == 400


def test_release_flow(client):
    pid = client.post("/profiles", json=_payload()).json()["id"]
    rel = client.post(f"/profiles/{pid}/release")
    assert rel.status_code == 200
    assert rel.json()["status"] == "released"

    listed = client.get("/profiles", params={"status": "released"})
    assert len(listed.json()) == 1


def test_missing_profile(client):
    r = client.get("/profiles/does-not-exist")
    assert r.status_code == 404
