
import pytest
from playwright.sync_api import Page, expect

# ---- setup: runs before EACH test -------
def test_page_title(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    expect(page).to_have_title("The Internet")

# ---- Login test ------
def test_valid_login(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("You logged into a secure area!")).to_be_visible()

# ---- Negative test ---------
def test_invalid_login(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill("wronguser")
    page.get_by_label("Password").fill("wrongpass")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash.error")).to_contain_text("Your username is invalid!")