# Day 19 challenge — use every assertion type

"""
Test 1 — to_be_visible and to_be_hidden
Go to /login. Assert flash message is hidden before login. Submit wrong credentials. 
Assert flash error is now visible. Assert flash contains "Your username is invalid".

Test 2 — to_have_value and to_have_attribute
Go to /login. Fill username with "tomsmith". Assert to_have_value("tomsmith"). 
Assert username input has attribute type="text". Assert password input has attribute type="password".

Test 3 — to_have_count with dynamic content
Go to /add_remove_elements/. Assert Delete button count is 0. Click Add Element 4 times. 
Assert count is 4. Click Delete twice. Assert count is 2.

Test 4 — to_be_checked and not_to_be_checked
Go to /checkboxes. Assert initial state (first unchecked, second checked). 
Check first, uncheck second. Assert state flipped. Assert to_have_count(2) still passes.

Test 5 — to_have_url after navigation
Go to homepage. Click the "Dropdown" link. Assert URL is /dropdown. Select option 1. 
Assert to_have_value("1") and to_contain_text("Option 1"). Select option 2. Assert to_have_value("2").

Test 6 — custom timeout
Go to /login. Assert the Login button is visible with a custom timeout=10000 (10 seconds). 
Assert the heading is visible with timeout=5000.
"""

# ================================================================================================================

import pytest
from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

# ----- Test 1: visible/hidden -------------------------
def test_visible_and_hidden(page: Page):
    page.goto(f"{BASE}/login")

    # Flash is hidden before any action
    expect(page.locator("#flash")).to_be_hidden()

    # Submit wrong credentials 
    page.get_by_label("Username").fill("wronguser")
    page.get_by_label("Password").fill("wrongpass")
    page.get_by_role("button", name="Login").click()

    # Flash error is now visible
    expect(page.locator("#flash.error")).to_be_visible()
    expect(page.locator("#flash.error")).to_contain_text("Your username is invalid")

# --- Test 2: to_have_value + to_have_attribute --------------
def test_value_and_attribute(page: Page):
    page.goto(f"{BASE}/login")

    page.get_by_label("Username").fill("tomsmith")
    expect(page.get_by_label("Username")).to_have_value("tomsmith")

    # Assert input type attribute
    expect(page.locator("#username")).to_have_attribute("type", "text")
    expect(page.locator("#password")).to_have_attribute("type", "password")

# ----- Test 3: to_have_count with dynamic content -------------------
def test_dynamic_count(page: Page):
    page.goto(f"{BASE}/add_remove_elements/")
    delete_btns = page.get_by_role("button", name="Delete")
    add_btn = page.get_by_role("button", name="Add Element")

    # Initially no delete buttons
    expect(delete_btns).to_have_count(0)

    # Add 4
    for _ in range(4):
        add_btn.click()
    expect(delete_btns).to_have_count(4)

    # Remove 2
    for _ in range(2):
        delete_btns.first.click()
    expect(delete_btns).to_have_count(2)

# ---- Test 4: to_be_checked / not_to_be_checked ------------------
def test_checkbox_state(page: Page):
    page.goto(f"{BASE}/checkboxes")
    checkboxes = page.locator("input[type='checkbox']")

    # Assert initial state
    expect(checkboxes.first).not_to_be_checked()
    expect(checkboxes.last).to_be_checked()

    # Flip both
    checkboxes.first.check()
    checkboxes.last.uncheck()

    # Assert flipped
    expect(checkboxes.first).to_be_checked()
    expect(checkboxes.last).not_to_be_checked()

    # Count still correct after interactions
    expect(checkboxes).to_have_count(2)

#----- Test 5: to_have_url after navigation --------------
def test_url_and_dropdown(page: Page):
    page.goto(f"{BASE}")
    page.get_by_role("link", name="Dropdown", exact=True).click()
    expect(page).to_have_url(f"{BASE}/dropdown")

    dropdown = page.locator("#dropdown")

    dropdown.select_option("1")
    expect(dropdown).to_have_value("1")
    expect(dropdown).to_contain_text("Option 1")

    dropdown.select_option("2")
    expect(dropdown).to_have_value("2")

# ---- Test 6: custom timeout -------------------------------------
def test_custom_timeout(page: Page):
    page.goto(f"{BASE}/login")

    # Custom timeouts - milliseconds
    expect(page.get_by_role("button", name="Login")).to_be_visible(timeout=10000)

    expect(page.get_by_role("heading", name="Login Page", exact=True)).to_be_visible(timeout=5000)