from playwright.sync_api import Page, expect

def test_page_title(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    expect(page).to_have_title("The Internet")