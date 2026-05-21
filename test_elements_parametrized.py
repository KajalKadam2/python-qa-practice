# Example 2 — Dropdown + checkbox parametrized 

import pytest
from playwright.sync_api import Page, expect

# --- Dropdown ------------------------------------------------------------------
@pytest.mark.parametrize("option_value, expected_value", [
    ("1", "1"),
    ("2", "2")
], ids=["select_option_1", "select_option_2"])
def test_dropdown_options(dropdown_page: Page, option_value, expected_value):
    dropdown_page.locator("#dropdown").select_option(option_value)
    expect(dropdown_page.locator("#dropdown")).to_have_value(expected_value)

#----- checkboxes ----------------------------------------------------------------
@pytest.mark.parametrize("index, initial_state, action", [
    (0, False, "check"),   #First box starts unchecked, check it
    (1, True, "uncheck"), #second box starts checked, uncheck it
], ids=["check_first", "uncheck_second"])
def test_checkbox_interaction(checkboxes_page: Page, index, initial_state, action):
    checkbox = checkboxes_page.locator("input[type='checkbox']").nth(index)

    # Assert initial state
    if initial_state:
        expect(checkbox).to_be_checked()
    else:
        expect(checkbox).not_to_be_checked
    
    # Perform action
    if action == "check":
        checkbox.check()
        expect(checkbox).to_be_checked()
    else:
        checkbox.uncheck()
        expect(checkbox).not_to_be_checked()
        