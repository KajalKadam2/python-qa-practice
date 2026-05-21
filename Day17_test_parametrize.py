# Basic parametrize syntax

import pytest
from playwright.sync_api import Page, expect

# --- Single parameter ------------
@pytest.mark.parametrize("path", [
    "/login",
    "/checkboxes",
    "/dropdown",
    "/add_remove_elements",
])
def test_pages_load(page: Page, path):
    page.goto(f"https://the-internet.herokuapp.com{path}")
    # Assert URL loaded correctly instead of title
    expect(page).to_have_url(f"https://the-internet.herokuapp.com{path}")

# ---- multiple parameters ------------
@pytest.mark.parametrize("username, password, expected", [
    ("tomsmith",  "SuperSecretPassword!", "secure area"),
    ("wronguser", "wrongpass",            "Your username is invalid"),
    ("tomsmith",  "wrongpass",            "Your password is invalid"),
    ("",          "",                     "Your username is invalid"),
])

def test_login_scenarios(page: Page, username, password, expected):
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text(expected)


# ---- parametrize + fixtures together ----------------------

# login_page fixture from conftest.py handles navigation
# parametrize handles the test data

@pytest.mark.parametrize("username, password, expected_text", [
    ("tomsmith",  "SuperSecretPassword!", "secure area"),
    ("wronguser", "wrongpass",            "Your username is invalid"),
    ("tomsmith",  "wrongpass",            "Your password is invalid"),
    ("",          "",                     "Your username is invalid"),
    ("TOMSMITH",  "SuperSecretPassword!", "Your username is invalid"),
], ids=[
    "valid", "wrong_user", "wrong_pass", "empty", "uppercase_user"
])

def test_login(login_page: Page, username, password, expected_text):
    # login_page fixture already navigated to /login
    login_page.get_by_label("Username").fill(username)
    login_page.get_by_label("Password").fill(password)
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash")).to_contain_text(expected_text)