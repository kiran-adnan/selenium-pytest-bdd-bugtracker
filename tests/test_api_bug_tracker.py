import requests

BASE = "http://127.0.0.1:5000"

def test_create_bug_and_list():
    # Create
    r = requests.post(f"{BASE}/bugs", json={"title": "UI alignment issue", "severity": "High", "status": "Open"})
    assert r.status_code == 201
    bug = r.json()
    assert bug["title"] == "UI alignment issue"
    assert bug["severity"] == "High"
    assert bug["status"] == "Open"
    bug_id = bug["id"]

    # List contains it
    r = requests.get(f"{BASE}/bugs")
    assert r.status_code == 200
    bugs = r.json()
    assert any(b["id"] == bug_id for b in bugs)

def test_update_status_then_delete():
    # Create
    r = requests.post(f"{BASE}/bugs", json={"title": "Crash on save", "severity": "Critical", "status": "Open"})
    assert r.status_code == 201
    bug_id = r.json()["id"]

    # Update
    r = requests.put(f"{BASE}/bugs/{bug_id}", json={"status": "Closed"})
    assert r.status_code == 200
    assert r.json()["status"] == "Closed"

    # Delete
    r = requests.delete(f"{BASE}/bugs/{bug_id}")
    assert r.status_code == 204

    # Ensure gone
    r = requests.get(f"{BASE}/bugs")
    assert r.status_code == 200
    assert all(b["id"] != bug_id for b in r.json())