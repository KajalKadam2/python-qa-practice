# CheckboxesPage — a second page object

from playwright.sync_api import Page, expect
from pages.base_page import BasePage

BASE_URL = "https://the-internet.herokuapp.com"


class CheckboxesPage(BasePage):
    """ Page object for the checkboxes page. """

    URL = f"{BASE_URL}/checkboxes"

    # --- Locators ----------------------------------
    def checkbox(self, index: int):
        """ Return checkbox at given index (0 or 1). """
        return self.page.locator("input[type='checkbox']").nth(index)
    
    @property
    def first_checkbox(self):
        return self.checkbox(0)
    
    @property
    def second_checkbox(self):
        return self.checkbox(1)
    
    # ---- Actions ---------------------------------
    def open(self) -> "CheckboxesPage":
        self.page.goto(self.URL)
        return self
    
    def check_first(self) -> "CheckboxesPage":
        self.first_checkbox.check()
        return self
    
    def uncheck_second(self) -> "CheckboxesPage":
        self.second_checkbox.uncheck()
        return self
    
    def check_second(self) -> "CheckboxesPage":
        self.second_checkbox.uncheck()
        return self
    
    # --- Assertions -----------------------------------
    def expect_first_unchecked(self) -> "CheckboxesPage":
        expect(self.first_checkbox).not_to_be_checked()
        return self
    
    def expect_first_checked(self) -> "CheckboxesPage":
        expect(self.first_checkbox).to_be_checked()
        return self
    
    def expect_second_checked(self) -> "CheckboxesPage":
        expect(self.second_checkbox).to_be_checked()
        return self
    
    def expect_second_unchecked(self) -> "CheckboxesPage":
        expect(self.second_checkbox).not_to_be_checked()
        return self