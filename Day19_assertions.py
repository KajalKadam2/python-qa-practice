# visibility assertions

from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

def test_visibility_assertions(page: Page):
    page.goto(f"{BASE}/login")

    # Element is visible on screen
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    # Element is enabled (not greyed out)
    expect(page.get_by_label("Username")).to_be_enabled()

    # NOT assertions - the negative form
    expect(page.locator("#flash")).to_be_hidden() # flash not shown yet

def test_visible_after_Action(page: Page):
    page.goto(f"{BASE}/login")

    # Flash is hidden before login
    expect(page.locator("#flash")).to_be_hidden()

    # After failed login - flash appears
    page.get_by_label("Username").fill("wrong")
    page.get_by_label("Password").fill("wrong")
    page.get_by_role("button", name="Login").click()

    # Now flash is visible - expect retries until it appears
    expect(page.locator("#flash.error")).to_be_visible()


# ----- Text and value assertions ---------------------------------------------------------

def test_text_assertions(page: Page):
    page.goto(f"{BASE}/login")
    page.get_by_label("Username").fill("wrong")
    page.get_by_label("Password").fill("wrong")
    page.get_by_role("button", name="Login").click()

    flash = page.locator("#flash")

    # to_contain_text - partial match - most flexible
    expect(flash).to_contain_text("Your username is invalid")

    # to_have_text — full exact match including whitespace
    # Use to_contain_text unless you need the full string

def test_value_assertions(page: Page):
    page.goto(f"{BASE}/login")

    # Fill field - assert value was set correctly
    page.get_by_label("Username").fill("tomsmith")
    expect(page.get_by_label("Username")).to_have_value("tomsmith")

    # Dropdown value
    page.goto(f"{BASE}/dropdown")
    page.locator("#dropdown").select_option("1")
    expect(page.locator("#dropdown")).to_have_value("1")

def test_attribute_assertions(page: Page):
    page.goto(f"{BASE}/login")

    # Assert input type attribute
    expect(page.locator("#username")).to_have_attribute("type", "text")
    expect(page.locator("#password")).to_have_attribute("type", "password")


# ------- URL, title and count assertions --------------------------------------------------

def test_url_assertions(page: Page):
    page.goto(f"{BASE}/login")
    expect(page).to_have_url(f"{BASE}/login")

    # After login - URL changes to / secure
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(f"{BASE}/secure")

def test_count_assertions(page: Page):
    page.goto(f"{BASE}/checkboxes")
    expect(page.locator("input[type='checkbox']")).to_have_count(2)

def test_dynamic_count(page: Page):
    page.goto(f"{BASE}/add_remove_elements/")
    # No delete buttons initially
    expect(page.get_by_role("button", name="Delete")).to_have_count(0)

    # Add 2 elements
    page.get_by_role("button", name="Add Element").click()
    page.get_by_role("button", name="Add Element").click()
    expect(page.get_by_role("button", name="Delete")).to_have_count(2)

    # Remove one - count drops to 1
    page.get_by_role("button", name="Delete").first.click()
    expect(page.get_by_role("button", name="Delete")).to_have_count(1)


# ---- Checkbox, focus and state assertions -----------------------------------------------

def test_checkbox_assertions(page: Page):
    page.goto(f"{BASE}/checkboxes")
    first = page.locator("input[type='checkbox']").first
    second = page.locator("input[type='checkbox']").last

    # Initial state
    expect(first).not_to_be_checked()
    expect(second).to_be_checked()

    # Check first, uncheck second
    first.check()
    second.uncheck()

    # Assert state flipped
    expect(first).to_be_checked()
    expect(second).not_to_be_checked()

def test_editable_assertions(page: Page):
    page.goto(f"{BASE}/login")

    # Input should be editable
    expect(page.get_by_label("Username")).to_be_editable()
    expect(page.get_by_label("Password")).to_be_editable()


# ------ Soft assertions — collect all failures at once  ---------------------------------

def test_soft_assertions(page: Page):
    page.goto(f"{BASE}/login")

    # Create a soft assertion context
    soft = expect.soft(page)

    # All these run — even if one fails
    soft.to_have_url(f"{BASE}/login")
    soft.to_have_title("The Internet")

    # Soft assert on elements
    expect.soft(page.get_by_label("Username")).to_be_visible()
    expect.soft(page.get_by_label("Password")).to_be_visible()
    expect.soft(page.get_by_role("button", name="Login")).to_be_visible()

    # At the end — raises ALL failures at once if any failed
    page.context.pages[0]  # soft failures reported when test ends