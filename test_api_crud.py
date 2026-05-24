# PUT, PATCH, DELETE — complete CRUD coverage

import requests

BASE_URL = "https://reqres.in/api"
HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

# --- PUT - replace entire resource -----------
def test_update_user_put():
    payload = {"name": "Kajal Updated", "job": "Senior QA"}
    r = requests.put(f"{BASE_URL}/users/2", json=payload, headers=HEADERS)

    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Kajal Updated"
    assert body["job"] == "Senior QA"
    assert "updatedAt" in body

# --- PATCH - update partial resource ------------------
def test_update_user_patch():
    payload = {"job": "SDET"} # only updating job
    r = requests.patch(f"{BASE_URL}/users/2", json=payload, headers=HEADERS)

    assert r.status_code == 200
    body = r.json()
    assert body["job"] == "SDET"
    assert "updatedAt" in body

# --- DELETE - remove resources -------------
def test_delete_user():
    r = requests.delete(f"{BASE_URL}/users/2", headers=HEADERS)

    assert r.status_code == 204
    assert r.text == "" #204 no Content - body must be empty

# --- Login - POST with auth ------------------
def test_login_success():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    r = requests.post(f"{BASE_URL}/login",json=payload, headers=HEADERS)

    assert r.status_code == 200
    body = r.json()
    assert "token" in body
    assert len(body["token"]) > 0

def test_login_missing_password():
    payload = {"email": "eve.holt@reqres.in"} #no password
    r = requests.post(f"{BASE_URL}/login",json=payload, headers=HEADERS)

    assert r.status_code == 400
    body = r.json()
    assert "error" in body
    assert body["error"] == "Missing password"
