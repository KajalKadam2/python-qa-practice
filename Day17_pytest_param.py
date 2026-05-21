# pytest.param — marks and expected failures 

import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("username, password, expected", [
    # Normal test case
    ("tomsmith", "SuperSecretPassword!", "secure area"),
    ("wronguser", "wrongpass", "Your username is invalid"),

    # pytest.param with custom id
    pytest.param(
        "tomsmith", "wrongpass", "Your password is invalid",
        id="wrong_password_only"
    ),

    # pytest.param with xfail - known bug, documented
    pytest.param(
        "tomsmith", "SuperSecretPassword!", "secure area",
        id="leading_space_in_username",
        marks=pytest.mark.xfail(reason="Bug #42: spaces not trimmed")
    ),

    # pytest.param with skip
    pytest.param(
        "admin", "admin", "secure area",
        id="admin_user",
        marks=pytest.mark.skip(reason="admin user not set up in this env")
    ),
])

def test_login_with_marks(page: Page, username, password, expected):
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text(expected)