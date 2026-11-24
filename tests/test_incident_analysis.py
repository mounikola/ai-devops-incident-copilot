from fastapi.testclient import TestClient
from app.main import app

def test_upstream_failure():
    r = TestClient(app).post("/api/incidents/analyze", json={
        "title": "Checkout 502", "description": "Requests failing",
        "logs": "upstream connection refused"
    })
    assert r.status_code == 200
    assert r.json()["severity"] == "high"
    assert "connection refused" in r.json()["evidence"]
