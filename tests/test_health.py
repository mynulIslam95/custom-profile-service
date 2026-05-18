def test_health_includes_version(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "version" in r.json()


def test_ready_503(client):
    from src.app import set_ready

    set_ready(False)
    r = client.get("/ready")
    assert r.status_code == 503
