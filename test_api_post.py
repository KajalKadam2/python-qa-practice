# POST requests — creating resources

import requests
import pytest

BASE_URL = "https://reqres.in/api"
HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

def test_create_user_status_201():
    payload = {"name": "Kajal", "job": "QA Engineer"}
    r = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)
    assert r.status_code == 201

def test_create_user_body():
    payload = {"name": "Kajal", "job": "QA Engineer"}
    r = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)
    body = r.json()

    # Assert the created resources echoes back our back
    assert body["name"] == "Kajal"
    assert body["job"] == "QA Engineer"

    # Assert the API assigned an ID and timestamp
    assert "id" in body
    assert "createdAt" in body
    assert body["id"] 
    assert body["createdAt"]

def test_create_user_id_is_string():
    """ reqres returns id as a string - verify the type. """
    payload = {"name": "Test", "job": "Tester"}
    r = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)
    body = r.json()
    assert isinstance(body["id"], str), f"Expected str, got {type(body['id'])}"

# Parametrized POST
@pytest.mark.parametrize("name, job", [
    ("Alice", "Developer"),
    ("Bob", "Designer"),
    ("Kajal", "QA Engineer"),
], ids = ["developer", "designer", "qa_engineer"])

def test_create_various_users(name, job):
    r = requests.post(f"{BASE_URL}/users", json={"name": name, "job": job}, headers=HEADERS)
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == name
    assert body["job"] == job
