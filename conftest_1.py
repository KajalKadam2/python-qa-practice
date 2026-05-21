# conftest.py — sharing fixtures across all test files 

import pytest
from playwright.sync_api import Page
from pathlib import Path

BASE_URL = "https://the-internet.herokuapp.com"

@pytest.fixture
def login_page(page: Page):
    page.goto(f"{BASE_URL}/login")
    yield page

@pytest.fixture
def logged_in_page(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    yield page

@pytest.fixture
def checkboxes_page(page: Page):
    page.goto(f"{BASE_URL}/checkboxes")
    yield page

@pytest.fixture
def dropdown_page(page: Page):
    page.goto(f"{BASE_URL}/dropdown")
    yield page

@pytest.fixture
def valid_user():
    return {
        "username": "tomsmith",
        "password": "SuperSecretPassword!",
        "success_msg": "You logged into a secure area!"
    }

# ------ Auto screenshot on test failure ---------------
@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    """ Automatically screenshot any failing test """
    yield # test runs here

    # After test - check if it failed
    if request.node.rep_call.failed:
        #Create screenshots folder if needed
        Path("screenshots").mkdir(exist_ok=True)

        # Safe filename from test name
        test_name = request.node.name.replace("[","-").replace("]","")
        path = f"screenshots/{test_name}.png"
        page.screenshot(path=path, full_page=True)
        print(f"\n 📸 Screenshot saved: {path}")

# This hook makes request.node.rep_call available
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)