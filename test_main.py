from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- Existing /calculate tests ---
def test_basic_division():
    r = client.post("/calculate", json={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", json={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", json={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", json={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""

# --- GET /history tests ---
def test_get_history_empty():
    client.delete("/history")
    r = client.get("/history")
    assert r.status_code == 200
    assert r.json() == []

def test_get_history_after_calc():
    client.delete("/history")
    client.post("/calculate", json={"expr": "17 + 10"})
    r = client.get("/history")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["expr"] == "17 + 10"

def test_get_history_limit_param():
    client.delete("/history")
    client.post("/calculate", json={"expr": "1+1"})
    client.post("/calculate", json={"expr": "2+2"})
    r = client.get("/history", params={"limit": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1

# --- DELETE /history tests ---
def test_delete_history_response():
    r = client.delete("/history")
    assert r.status_code == 200
    assert r.json() == {"ok": True, "cleared": True}

def test_delete_history_clears_data():
    client.post("/calculate", json={"expr": "5*5"})
    client.delete("/history")
    r = client.get("/history")
    assert r.json() == []

def test_delete_history_already_empty():
    client.delete("/history")
    r = client.delete("/history")
    assert r.status_code == 200
    assert r.json()["cleared"] is True

def test_calculate_endpoint():
    # Pass json body matching Expression schema
    response = client.post("/calculate", json={"expr": "100 + 50"})
    assert response.status_code == 200
    assert response.json()["result"] == 150