# test_fixtures_yield_day15
# yield — running code after the test teardown pattern


import pytest
from playwright.sync_api import Page, expect

@pytest.fixture

def authenticated_page(page: Page):
    """ Log in before the test, logout after """
    # SETUP - login
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    print("\n -> Setup: logged in successfully")

    yield page # test runs here

    # TEARDOWN - click logout
    page.get_by_role("link", name="Logout").click()
    print("\n -> Teardown: logged out")

def test_secure_area_visible(authenticated_page: Page):
    expect(authenticated_page.get_by_role("heading", name="Secure Area", exact=True)).to_be_visible()

def test_logout_link_visible(authenticated_page: Page):
    expect(authenticated_page.get_by_role("link", name="Logout")).to_be_visible()