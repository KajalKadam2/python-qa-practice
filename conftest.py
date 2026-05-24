import pytest
from playwright.sync_api import Page
from pathlib import Path
from pages.login_page import LoginPage
from pages.checkboxes_page import CheckboxesPage

BASE_URL = "https://the-internet.herokuapp.com"


# --- Storing parametrize data in conftest.py ----

INVALID_LOGIN_CASES = [
    pytest.param("wronguser", "wrongpass",            "Your username is invalid", id="wrong_user"),
    pytest.param("tomsmith",  "wrongpass",            "Your password is invalid", id="wrong_pass"),
    pytest.param("",          "",                     "Your username is invalid", id="empty"),
]

DROPDOWN_OPTIONS = [
    pytest.param("1", "1", id="option1"),
    pytest.param("2", "2", id="option2"),
]

# ── Page fixtures ────────────────────────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def login_page(page: Page):
    """Navigate to login page before each test."""
    page.goto(f"{BASE_URL}/login")
    yield page

@pytest.fixture
def logged_in_page(page: Page):
    """Login and land on secure area."""
    page.goto(f"{BASE_URL}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    yield page

@pytest.fixture
def checkboxes_page(page: Page):
    """Navigate to checkboxes page."""
    page.goto(f"{BASE_URL}/checkboxes")
    yield page

@pytest.fixture
def dropdown_page(page: Page):
    """Navigate to dropdown page."""
    page.goto(f"{BASE_URL}/dropdown")
    yield page

# ── Data fixtures ────────────────────────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def valid_user():
    """Valid login credentials."""
    return {
        "username": "tomsmith",
        "password": "SuperSecretPassword!",
        "success_msg": "You logged into a secure area!"
    }

# ── Screenshot on failure ────────────────────────────────────────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        Path("screenshots").mkdir(exist_ok=True)
        name = request.node.name.replace("[", "_").replace("]", "")
        page.screenshot(path=f"screenshots/{name}.png", full_page=True)
        print(f"\n  📸 Screenshot: screenshots/{name}.png")


# ── POM fixtures ─────────────────────────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def login_page_pom(page: Page) -> LoginPage:
    """Returns a LoginPage object navigated to the login URL."""
    lp = LoginPage(page)
    lp.open()
    yield lp

@pytest.fixture
def logged_in_pom(page: Page) -> LoginPage:
    """Returns LoginPage already logged in."""
    lp = LoginPage(page)
    lp.open().login("tomsmith", "SuperSecretPassword!")
    yield lp

@pytest.fixture
def checkboxes_pom(page: Page) -> CheckboxesPage:
    """Returns a CheckboxesPage object navigated to checkboxes."""
    cp = CheckboxesPage(page)
    cp.open()
    yield cp