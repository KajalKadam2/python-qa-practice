# Day 18 challenge — use every locator type

# Write these 6 tests — one per locator type
""" 
Test 1 — get_by_role
Go to /add_remove_elements. Use get_by_role to click "Add Element" 3 times. 
Assert 3 Delete buttons are visible using to_have_count(3).

Test 2 — get_by_label
Go to /login. Use get_by_label for both inputs. Login with valid credentials. 
Assert URL contains /secure.

Test 3 — get_by_text
Go to the homepage. Use get_by_text to click the "Hovers" link. 
Assert URL is /hovers. Use exact=True.

Test 4 — CSS selector
Go to /checkboxes. Use CSS input[type='checkbox'] with .first and .last. 
Assert first is unchecked, last is checked. Then check the first. Assert both are now checked.

Test 5 — XPath
Go to /login. Use XPath //*[@id='username'] and //*[@id='password'] to fill the form. 
Use //button[@type='submit'] to click. Assert success flash visible.

Test 6 — .nth() + .filter()
Go to /dropdown. Use CSS #dropdown to select option "2". Assert to_have_value("2") 
AND to_contain_text("Option 2").
"""

# ==========================================================================================================

import pytest
from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

# --- Test 1: get_by_role ----------------------------
def test_add_remove_with_role(page: Page):
    page.goto(f"{BASE}/add_remove_elements/")
    add_btn = page.get_by_role("button", name="Add Element")

    for _ in range(3):
        add_btn.click()
    
    expect(
        page.get_by_role("button", name="Delete")
    ).to_have_count(3)

#---- Test 2: get_by_label --------------------------------
def test_login_with_label(page: Page):
    page.goto(f"{BASE}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(f"{BASE}/secure")

#---- Test 3: get_by_text -----------------------------------
def test_navigation_with_text(page: Page):
    page.goto(f"{BASE}")
    page.get_by_role("link", name="Hovers", exact=True).click()
    expect(page).to_have_url(f"{BASE}/hovers")

#---- Test 4: CSS selector ----------------------------------
def test_checkboxes_with_css(page: Page):
    page.goto(f"{BASE}/checkboxes")
    checkboxes = page.locator("input[type='checkbox']")

    # Assert initial state
    expect(checkboxes.first).not_to_be_checked()
    expect(checkboxes.last).to_be_checked()

    # Check the first checkbox
    checkboxes.first.check()

    # Both should now be checked
    expect(checkboxes.first).to_be_checked()
    expect(checkboxes.last).to_be_checked()

#---- Test 5: XPath ---------------------------------------------
def test_login_with_xpath(page: Page):
    page.goto(f"{BASE}/login")
    page.locator("//*[@id='username']").fill("tomsmith")
    page.locator("//*[@id='password']").fill("SuperSecretPassword!")
    page.locator("//button[@type='submit']").click()
    expect(page.locator("//div[@id='flash']")).to_contain_text("secure area")

#---- Test 6: nth + dropdown --------------------------------------
def test_dropdown_with_css(page: Page):
    page.goto(f"{BASE}/dropdown")
    page.locator("#dropdown").select_option("2")
    expect(page.locator("#dropdown")).to_have_value("2")
    expect(page.locator("#dropdown")).to_contain_text("Option 2")