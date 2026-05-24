# pages/base_page.py

from playwright.sync_api import Page, expect

class BasePage:
    """ Base class for all page objects.
    Contains shared methods every page uses. """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> "BasePage":
       """ Navigate to a URL. Returns self for chaining. """
       self.page.goto(url)
       return self
    
    def get_title(self) -> str:
       """ Return the current page title. """
       return self.page.title()
    
    def get_url(self) -> str:
        """ Return the current page URL. """
        return self.page.url
    
    def expect_title(self, title: str) -> "BasePage":
        """ Assert the page title matches. """
        expect(self.page).to_have_title(title)
        return self
    
    def screenshot(self, name: str) -> "BasePage":
        """ Take a screenshot. Returns self for chaining. """
        self.page.screenshot(path=f"screenshot/{name}.png", full_page=True)
        return self 