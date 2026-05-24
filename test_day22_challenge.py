# test_day22_challenge

"""
Write these 5 test functions
Test 1 — test_get_all_users_schema
GET /users?page=2. Assert: status 200, page==2, total==12, per_page==6, len(data)==6, 
every user has id/email/first_name/last_name/avatar fields.

Test 2 — test_create_and_verify_user
POST /users with your own name and job. Assert: status 201, response echoes name and job, 
id is present and non-empty, createdAt is present, id is a string type.

Test 3 — test_login_parametrized
Parametrize at least 4 login scenarios (valid, no password, no email, wrong email). For each: assert 
correct status code, assert body has "token" key on success or "error" key on failure. Use ids=.

Test 4 — test_user_ids_parametrized
Parametrize GET /users/{id} for IDs 1-6 (valid, 200) and IDs 0, 99, 999 (invalid, 404). 
Two separate parametrized functions or one function with a status code parameter.

Test 5 — test_update_then_verify
PATCH /users/2 with a new job title. Assert: status 200, job field matches what you sent, 
updatedAt field exists. Then PATCH again with a different job. Assert the new job is reflected.
"""

# ===================================================================================================
import pytest
import requests

BASE_URL = "https://reqres.in/api"
HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

# ----- Test 1: GET /users/page=2 schema --------------------
def test_get_all_users_schema():
    r = requests.get(f"{BASE_URL}/users", params={"page": 2}, headers=HEADERS)

    assert r.status_code == 200
    body = r.json()

    # Pagination fields
    assert body["page"] == 2
    assert body["total"] == 12
    assert body["per_page"] == 6
    assert len(body["data"]) == 6

    #Every user has required fields
    required = ["id", "email", "first_name", "last_name", "avatar"]
    for user in body["data"]:
        for field in required:
            assert field in user, f"User {user.get('id')} missing '{field}'"

#------ Test 2 : POST /users create and verify -----------------
def test_create_and_verify_user():
    payload = {"name": "Kajal Kadam", "job": "QA Engineer"}
    r = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)

    assert r.status_code == 201
    body = r.json()

    #Response echoes our data
    assert body["name"] == "Kajal Kadam"
    assert body["job"] == "QA Engineer"

    #API assigned id and timestamp
    assert "id" in body
    assert "createdAt" in body
    assert body["id"] #truthy - not empty
    assert body["createdAt"] #truthy - timestamp present

    #id is a string type (reqres returns id as string)
    assert isinstance(body["id"], str), (f"Expected id to be str, got {type(body['id']).__name__}")

#---- Test 3: login parametrized ------------------------------
@pytest.mark.parametrize("email, password, expected_status, expect_token", [
    ("eve.holt@reqres.in",   "cityslicka", 200, True),
    ("eve.holt@reqres.in",   "",            400, False),
    ("",                      "cityslicka", 400, False),
    ("notfound@reqres.in",    "anypass",    400, False),
], ids=["valid", "no_password", "no_email", "not_registered"])

def test_login_parametrized(email, password, expected_status, expect_token):
    r = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password}, headers=HEADERS)

    assert r.status_code == expected_status
    body = r.json()
    if expect_token:
        assert "token" in body
        assert len(body["token"]) > 0
    else:
        assert "error" in body

#---- Test 4a : valid user IDs -> 200 -----------------------
@pytest.mark.parametrize("user_id", [1,2,3,4,5,6], ids=[f"user_{i}" for i in range(1, 7)])

def test_valid_user_ids_return_200(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)

    assert r.status_code == 200
    assert r.json()["data"]["id"] == user_id

#---- Test 4b : invalid user IDs -> 404---------------------
@pytest.mark.parametrize("user_id", [0,99,999], ids=["zero", "ninety_nine", "nine_ninety_nine"])

def test_invalid_user_ids_return_404(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)

    assert r.status_code == 404

#---- Test 5 : PATCH update then verify -------------------------------------------------------
def test_update_then_verify():

    # First update
    r = requests.patch(f"{BASE_URL}/users/2", json={"job": "Senior QA Engineer"}, headers=HEADERS)

    assert r.status_code == 200
    body = r.json()
    assert body["job"] == "Senior QA Engineer"
    assert "updatedAt" in body

    # Second update - different job
    r = requests.patch(f"{BASE_URL}/users/2", json={"job": "SDET"}, headers=HEADERS)

    assert r.status_code == 200
    assert r.json()["job"] == "SDET"