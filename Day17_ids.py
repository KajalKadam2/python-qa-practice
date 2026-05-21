#  ids= — giving test cases readable names 

import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("username, password, expected", [
    ("tomsmith",  "SuperSecretPassword!", "secure area"),
    ("wronguser", "wrongpass",            "Your username is invalid"),
    ("tomsmith",  "wrongpass",            "Your password is invalid"),
    ("",          "",                     "Your username is invalid"),
], ids=[
    "valid_credentials",
    "wrong_username",
    "wrong_password",
    "empty_fields",
])

def test_login_scenarios(page: Page, username, password, expected):
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text(expected)