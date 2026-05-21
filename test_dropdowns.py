# test_dropdowns.py

from playwright.sync_api import Page, expect

def test_default_option(dropdown_page: Page):
    expect(dropdown_page.locator("#dropdown")).to_be_visible()

def test_select_option1(dropdown_page: Page):
    dropdown_page.locator("#dropdown").select_option("1")
    expect(dropdown_page.locator("#dropdown")).to_have_value("1")

def test_select_option2(dropdown_page: Page):
    dropdown_page.locator("#dropdown").select_option("2")
    expect(dropdown_page.locator("#dropdown")).to_have_value("2")