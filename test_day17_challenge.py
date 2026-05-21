# Day 17 challenge 

""" 
Build a complete parametrized test file
Write these 4 parametrized test functions:

Test 1 — test_pages_load
Parametrize 5 paths: /login, /checkboxes, /dropdown, /add_remove_elements, /hovers. Each should load and 
show title "The Internet". Use ids= with short names.

Test 2 — test_login_scenarios
Combine valid + invalid in one parametrized function using login_page fixture. 
At least 5 scenarios. Use ids=. Add one xfail case for a known edge case.

Test 3 — test_add_remove_elements
Go to /add_remove_elements. Parametrize: click Add Element 1 time, 2 times, 3 times. 
After each: assert the correct number of Delete buttons are visible using to_have_count(n).

Test 4 — test_dropdown_then_verify
Parametrize selecting Option 1 and Option 2. After selecting, assert both to_have_value() 
AND that the selected option text is visible on the page.

"""

import pytest
from playwright.sync_api import Page, expect

# --- Test 1: pages load -----------------------------------------------
@pytest.mark.parametrize("path", [
    "/login",
    "/checkboxes",
    "/dropdown",
    "/add_remove_elements",
    "/hovers"
], ids=["login", "checkboxes", "dropdown", "add_remove", "hovers"])

def test_pages_load(page: Page, path):
    """ Each path should load - assert URL matches """
    page.goto(f"https://the-internet.herokuapp.com{path}")
    expect(page).to_have_url(f"https://the-internet.herokuapp.com{path}")

# --- Test 2: login scenarios ----------------------------------------------
@pytest.mark.parametrize("username, password, expected", [
    ("tomsmith",  "SuperSecretPassword!", "secure area"),
    ("wronguser", "wrongpass",            "Your username is invalid"),
    ("tomsmith",  "wrongpass",            "Your password is invalid"),
    ("",          "",                     "Your username is invalid"),
    ("tomsmith",  "SuperSecretPassword!", "secure area"),

    pytest.param(
        " tomsmith", "SuperSecretPassword!", "secure area",
        marks=pytest.mark.xfail(reason="Bug: leading spaces not trimmed")
    ),
], ids=[
    "valid", "wrong_user", "wrong_pass", "empty", "valid_again", "leading_space"
])

def test_login_scenarios(login_page: Page, username, password, expected):
    login_page.get_by_label("Username").fill(username)
    login_page.get_by_label("Password").fill(password)
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("#flash")).to_contain_text(expected)

# ---- Test 3: add/remove elements count ---------------------------------------
@pytest.mark.parametrize("click_count", [1,2,3],
                         ids=["one_click", "two_clicks", "three_clicks"])

def test_add_remove_elements(page: Page, click_count):
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    add_btn = page.get_by_role("button", name="Add Element")

    for _ in range(click_count):
        add_btn.click()
    
    expect(page.get_by_role("button", name="Delete")).to_have_count(click_count)


# ---- Test 4: dropdown selection + verify text ---------------------------
@pytest.mark.parametrize("value, label", [
    ("1", "Option 1"),
    ("2", "Option 2"),
], ids=["option_1", "option_2"])

def test_dropdown_then_verify(dropdown_page: Page, value, label):
    dropdown_page.locator("#dropdown").select_option(value)
    expect(dropdown_page.locator("#dropdown")).to_have_value(value)
    expect(dropdown_page.locator("#dropdown")).to_contain_text(label)