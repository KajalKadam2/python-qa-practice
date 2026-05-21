# test_login.py

from playwright.sync_api import Page, expect

def test_valid_login(login_page: Page, valid_user):
    login_page.get_by_label("Username").fill(valid_user["username"])
    login_page.get_by_label("Password").fill(valid_user["password"])
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.get_by_text(valid_user["success_msg"])).to_be_visible()

def test_invalid_login(login_page: Page):
    login_page.get_by_label("Username").fill("wronguser")
    login_page.get_by_label("Password").fill("wrongpass")
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash.error")).to_contain_text("Your username is invalid!")

def test_empty_username(login_page: Page):
    login_page.get_by_label("Username").fill("")
    login_page.get_by_label("Password").fill("somepassword")
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash.error")).to_be_visible()

def test_after_login_url(logged_in_page: Page):
    expect(logged_in_page).to_have_url(f"https://the-internet.herokuapp.com/secure")