# test_from_conftest

# test_from_conftest.py
import pytest
from conftest import INVALID_LOGIN_CASES, DROPDOWN_OPTIONS
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("username, password, expected", INVALID_LOGIN_CASES)
def test_invalid_logins(login_page: Page, username, password, expected):
    login_page.get_by_label("Username").fill(username)
    login_page.get_by_label("Password").fill(password)
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash")).to_contain_text(expected)


@pytest.mark.parametrize("value, expected_value", DROPDOWN_OPTIONS)
def test_dropdown_selection(dropdown_page: Page, value, expected_value):
    dropdown_page.locator("#dropdown").select_option(value)
    expect(dropdown_page.locator("#dropdown")).to_have_value(expected_value)