# Day18_all_locators.py — complete locator reference

import pytest
from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

# ── Role locators ─────────────────────────────────
def test_role_locators(page: Page):
    page.goto(f"{BASE}/login")
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    expect(page.get_by_role("heading", name="Login Page", exact=True)).to_be_visible()

# ── Label locators ────────────────────────────────
def test_label_locators(page: Page):
    page.goto(f"{BASE}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash.success")).to_be_visible()

# ── CSS locators ──────────────────────────────────
def test_css_locators(page: Page):
    page.goto(f"{BASE}/checkboxes")
    expect(page.locator("input[type='checkbox']")).to_have_count(2)
    expect(page.locator("input[type='checkbox']").first).not_to_be_checked()
    expect(page.locator("input[type='checkbox']").last).to_be_checked()

# ── XPath locators ────────────────────────────────
def test_xpath_locators(page: Page):
    page.goto(f"{BASE}/login")
    page.locator("//*[@id='username']").fill("tomsmith")
    page.locator("//*[@id='password']").fill("SuperSecretPassword!")
    page.locator("//button[@type='submit']").click()
    expect(page.locator("//div[@id='flash']")).to_contain_text("secure area")

# ── nth, first, last ──────────────────────────────
def test_nth_locators(page: Page):
    page.goto(f"{BASE}/checkboxes")
    page.locator("input[type='checkbox']").nth(0).check()
    expect(page.locator("input[type='checkbox']").nth(0)).to_be_checked()

# ── Dropdown with CSS ─────────────────────────────
def test_dropdown_css(page: Page):
    page.goto(f"{BASE}/dropdown")
    page.locator("#dropdown").select_option("1")
    expect(page.locator("#dropdown")).to_have_value("1")