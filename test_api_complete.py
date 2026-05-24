#  Example — complete API test class 

import requests
import pytest



class ReqresAPI:
    """ Thin wrapper around reqres.in endpoints. """

    BASE = "https://reqres.in/api"
    HEADERS = {"x-api-key": "free_user_3E52AzI0czxneEVobhhCjAmWXCL"}

    def get_user(self, user_id: int):
        return requests.get(f"{self.BASE}/users/{user_id}", headers=self.HEADERS)
    
    def get_users(self, page: int = 1):
        return requests.get(f"{self.BASE}/users", params={"page": page}, headers=self.HEADERS)
    
    def create_user(self, name: str, job: str):
        return requests.post(f"{self.BASE}/users", json={"name": name, "job": job}, headers=self.HEADERS)
    
    def update_user(self, user_id: int, **kwargs):
        return requests.patch(f"{self.BASE}/users/{user_id}", json=kwargs, headers=self.HEADERS)
    
    def delete_user(self, user_id: int):
        return requests.delete(f"{self.BASE}/users/{user_id}", headers=self.HEADERS)
    
    def login(self, email: str, password: str):
        return requests.post(f"{self.BASE}/login", json={"email": email, "password": password}, headers=self.HEADERS)
    
@pytest.fixture
def api():
    return ReqresAPI()

#----- Tests ---------------------------------

def test_full_user_lifecycle(api):
    """ Created -> read -> update -> delete a user """

    # CREATE
    r = api.create_user("Kajal", "QA Engineer")
    assert r.status_code == 201
    user_id = r.json()["id"]

    # UPDATE (reqres is stateless - we update user 2)
    r = api.update_user(2, job="Senior QA")
    assert r.status_code == 200
    assert r.json()["job"] == "Senior QA"

    # DELETE
    r = api.delete_user(2)
    assert r.status_code == 204

def test_pagination(api):
    """ Both pages of users should return 6 items each. """
    for page in [1,2]:
        r = api.get_users(page=page)
        assert r. status_code == 200
        body = r.json()
        assert body["page"] == page
        assert len(body["data"]) == 6

def test_all_users_have_required_fields(api):
    """ Every user in the list must have id, email, first_name, last_name. """
    r = api.get_users()
    users = r.json()["data"]
    required = ["id", "email", "first_name", "last_name", "avatar"]
    for user in users:
        for field in required:
            assert field in user, f"User {user.get('id')} missing field '{field}'"