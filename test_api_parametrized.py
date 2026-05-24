# Parametrized API tests — data-driven at scale

import requests
import pytest

BASE_URL = "https://reqres.in/api"
HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

# --- Valid user IDs - should all return200 ----------
@pytest.mark.parametrize("user_id", [1,2,3,4,5,6], ids=[f"user_{i}" for i in range(1,7)])

def test_valid_users_return_200(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    assert r.status_code == 200
    assert r.json()["data"]["id"] == user_id

#--- Invalid user IDs - should all return 404 -----------
@pytest.mark.parametrize("user_id", [0,99,999,-1], 
                         ids=["zero", "ninety_nine", "nine_ninety_nine", "negative"])

def test_invalid_users_return_404(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    assert r.status_code == 404

#----- Login scenarios ---------------------------
@pytest.mark.parametrize("email, password, expected_status, has_token", [
    ("eve.holt@reqres.in", "cityslicka", 200, True),
    ("eve.holt@reqres.in", "",            400, False),
    ("",                   "cityslicka", 400, False),
    ("notregistered@x.com","pass",         400, False),
], ids=["valid", "no_password", "no_email", "not_registered"])

def test_login_scenarios(email, password, expected_status, has_token):
    r = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password}, headers=HEADERS)
    assert r.status_code == expected_status
    body = r.json()
    if has_token:
        assert "token" in body
    else:
        assert "error" in body