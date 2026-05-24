# Writing API tests with pytest

import requests
import pytest

BASE_URL = "https://reqres.in/api"
HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

# --- GET single user -----------------
def test_get_user_status_200():
    r = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    assert r.status_code == 200

def test_get_user_body_structure():
    r = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    body = r.json()

    # Assert top level keys exists
    assert "data" in body
    assert "support" in body

    # Assert user fields
    data = body["data"]
    assert data["id"] == 2
    assert data["email"] == "janet.weaver@reqres.in"
    assert data["first_name"] == "Janet"
    assert data["last_name"] == "Weaver"
    assert "avatar" in data
    assert data["avatar"].startswith("https://")

def test_get_user_not_found():
    r = requests.get(f"{BASE_URL}/users/99", headers=HEADERS) 
    assert r.status_code == 404
    assert r.json() == {}  #reqres returns empty body for 404

def test_get_user_content_type():
    r = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    assert "application/json" in r.headers["Content-Type"]

def test_get_user_response_time():
    r = requests.get(f"{BASE_URL}/users/2", headers=HEADERS)
    assert r.elapsed.total_seconds() < 3.0, (
        f"Too slow: {r.elapsed.total_seconds():.2f}s"
    )

# --- GET list of users ------------------------------
def test_get_users_list():
    r = requests.get(f"{BASE_URL}/users", params={"page": 1}, headers=HEADERS)
    assert r.status_code == 200

    body = r.json()
    assert body["page"] == 1
    assert body["per_page"] == 6
    assert len(body["data"]) == 6
    assert all("id" in u for u in body["data"])
    assert all("email" in u for u in body["data"])