# 

import pytest 
from playwright.sync_api import Page, expect

# --- Define a fixture -----------------
@pytest.fixture
def login_page(page: Page):
    """ Navigate to the login page before each test """
    page.goto("https://the-internet.herokuapp.com/login")
    return page      # hand the page back to test

# --- Use the fixture --------------
# Note: parameter name 'login_page' matches fixture name above
def test_valid_login(login_page: Page):
    login_page.get_by_label("Username").fill("tomsmith")
    login_page.get_by_label("Password").fill("SuperSecretPassword!")
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.get_by_text("You logged into a secure area!")).to_be_visible()

def test_invalid_login(login_page: Page):
    login_page.get_by_label("Username").fill("wronguser")
    login_page.get_by_label("Password").fill("wrongpass")
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash.error")).to_contain_text("Your username is invalid!")

def test_page_title(login_page: Page):
    expect(login_page).to_have_title("The Internet")