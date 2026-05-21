# test_checkboxes.py

from playwright.sync_api import Page, expect

def test_first_checkbox_unchecked(checkboxes_page: Page):
    first = checkboxes_page.locator("input[type='checkbox']").nth(0)
    expect(first).not_to_be_checked()

def test_check_first_checkbox(checkboxes_page: Page):
    first = checkboxes_page.locator("input[type='checkbox']").nth(0)
    first.check()
    expect(first).to_be_checked()

def test_second_checkbox_checked(checkboxes_page: Page):
    second = checkboxes_page.locator("input[type='checkbox']").nth(1)
    expect(second).to_be_checked()