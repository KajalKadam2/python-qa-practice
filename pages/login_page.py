# LoginPage — all login actions and locators in one place

from playwright.sync_api import Page, expect
from pages.base_page import BasePage

BASE_URL = "https://the-internet.herokuapp.com"


class LoginPage(BasePage):
    """ Page object for the login page. """

    # --- URL ------------------------
    URL = f"{BASE_URL}/login"

    # --- Locators - defined as properties ---
    @property
    def username_input(self):
        return self.page.get_by_label("Username")
    
    @property
    def password_input(self):
        return self.page.get_by_label("Password")
    
    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Login")
    
    @property
    def flash_message(self):
        return self.page.locator("#flash")
    
    @property
    def success_flash(self):
        return self.page.locator("#flash.success")
    
    @property
    def error_flash(self):
        return self.page.locator("#flash.error")
    
    # --- Actions -------------------
    def open(self) -> "LoginPage":
        """ Navigate to the login page. """
        self.page.goto(self.URL)
        return self
    
    def fill_username(self, username: str) -> "LoginPage":
        self.username_input.fill(username)
        return self

    def fill_password(self, password: str) -> "LoginPage":
        self.password_input.fill(password)
        return self
    
    def click_login(self) -> "LoginPage":
        self. login_button.click()
        return self
    
    def login(self, username: str, password: str) -> "LoginPage":
        """ Fill credentials and click Login - one-step action. """
        return (self
                .fill_username(username)
                .fill_password(password)
                .click_login())
    
    # --- Assertions -----------------------------
    def expect_success(self) -> "LoginPage":
        """ Assert login succeeded. """
        expect(self.success_flash).to_be_visible()
        expect(self.page).to_have_url(f"{BASE_URL}/secure")
        return self
    
    def expect_error(self, message: str) -> "LoginPage":
        """ Assert login failed with specific message. """
        expect(self.error_flash).to_be_visible()
        expect(self.error_flash).to_contain_text(message)
        return self
    
    def expect_on_login_page(self) -> "LoginPage":
        """ Assert we are still on the login page. """
        expect(self.page).to_have_url(self.URL)
        return self
