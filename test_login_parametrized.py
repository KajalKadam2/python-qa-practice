# Example 1 — Complete login test suite 

import pytest
from playwright.sync_api import Page, expect

# --- valid login scenario -------------------------------

@pytest.mark.parametrize("username, password", [
    ("tomsmith", "SuperSecretPassword!"),
], ids=["valid_user"])
def test_valid_logins(login_page: Page, username, password):
    login_page.get_by_label("Username").fill(username)
    login_page.get_by_label("Password").fill(password)
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash.success")).to_be_visible()
    expect(login_page).to_have_url("https://the-internet.herokuapp.com/secure")

# --- Invalid login scenarios ---------------------
@pytest.mark.parametrize("username, password, error_contains", [
    ("wronguser",  "SuperSecretPassword!", "Your username is invalid"),
    ("tomsmith",   "wrongpass",            "Your password is invalid"),
    ("",           "SuperSecretPassword!", "Your username is invalid"),
    ("tomsmith",   "",                     "Your password is invalid"),
    ("",           "",                     "Your username is invalid"),
    ("TomSmith",   "SuperSecretPassword!", "Your username is invalid"),
    ("tomsmith  ", "SuperSecretPassword!", "Your username is invalid"),
    ("' OR '1'='1","anything",             "Your username is invalid"),
], ids=[
    "wrong_username",
    "wrong_password",
    "empty_username",
    "empty_password",
    "both_empty",
    "case_sensitive",
    "trailing_space",
    "sql_injection",
])

def test_invalid_logins(login_page: Page, username, password, error_contains):
    login_page.get_by_label("Username").fill(username)
    login_page.get_by_label("Password").fill(password)
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash.error")).to_contain_text(error_contains)
    expect(login_page).to_have_url("https://the-internet.herokuapp.com/login")