# API fixtures — shared setup for API tests

import pytest
import requests

API_BASE_URL = "https://reqres.in/api"


@pytest.fixture
def api_base():
    """ Return the API base URL """
    return API_BASE_URL

@pytest.fixture
def auth_token():
    """ Get an auth token from the login endpoint """
    r = requests.post(
        f"{API_BASE_URL}/login",
        json={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )
    assert r.status_code == 200, "Login failed in fixture"
    return r.json()["token"]

@pytest.fixture
def created_user(api_base):
    """ Created a test user, yield it, nothing to clean up (reqres is stateless) """
    payload = {"name": "Test User", "job": "QA Engineer"}
    r = requests.post(f"{api_base}/users", json=payload)
    assert r.status_code == 201
    yield r.json() #yields the created user dict

#----- Tests using API fixtures ----------------------------
def test_user_has_id(created_user):
    assert "id" in created_user
    assert created_user["id"]

def test_token_is_string(auth_token):
    assert isinstance(auth_token, str)
    assert len(auth_token) > 5

def test_authenticated_request(api_base, auth_token):
    # Use token in Authorization header
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = requests.get(f"{api_base}/users", headers=headers)
    assert r.status_code == 200