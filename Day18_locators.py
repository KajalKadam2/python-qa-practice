# get_by_role()

from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

def test_get_by_role_button(page: Page):
    page.goto(f"{BASE}/login")

    # Find the login button by its role and name
    btn = page.get_by_role("button", name="Login")
    expect(btn).to_be_visible()
    expect(btn).to_be_enabled()

def test_get_by_role_heading(page: Page):
    page.goto(f"{BASE}/login")

    # exact = True prevents matching substrings
    heading = page.get_by_role("heading", name="Login Page", exact=True)
    expect(heading).to_be_visible()

def test_get_by_role_link(page: Page):
    page.goto(f"{BASE}")

    # Find a link by its text
    link = page.get_by_role("link", name="Form Authentication")
    expect(link).to_be_visible()
    link.click()
    expect(page).to_have_url(f"{BASE}/login")


#---- get by label -------------------------------------------------
def test_get_by_label(page: Page):
    page.goto(f"{BASE}/login")

    # Label "Username" is linked to the input via for= attribute
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")

    expect(page.get_by_label("Username")).to_have_value("tomsmith")

#------ get_by_placeholder --------------------------------------
def test_get_by_placeholder(page: Page):
    #input page has fields with placeholder text
    page.goto(f"{BASE}/inputs")

    number_input = page.get_by_role("spinbutton")
    number_input.fill("42")
    expect(number_input).to_have_value("42")

#--- get_by_text ------------------------------------
def test_get_by_text(page: Page):
    page.goto(f"{BASE}/login")

    #exact=True prevents strict mode violations
    expect(
        page.get_by_text("Login Page", exact=True)
    ).to_be_visible()

def test_get_by_text_link(page: Page):
    page.goto(f"{BASE}")

    #Click a link by its text
    page.get_by_text("Checkboxes").click()
    expect(page).to_have_url(f"{BASE}/checkboxes")

# ---------- locators()--------------------------------
def test_css_id_selector(page: Page):
    page.goto(f"{BASE}/login")

    # Use CSS ID selector for the username input
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.locator("button[type='submit']").click()
    expect(page.locator("#flash.success")).to_be_visible()

def test_css_attribute_selector(page: Page):
    page.goto(f"{BASE}/checkboxes")
    # target checkboxes by type attribute
    checkboxes = page.locator("input[type='checkbox']")
    expect(checkboxes).to_have_count(2)

def test_css_class_selector(page: Page):
    page.goto(f"{BASE}/login")
    page.locator("#username").fill("wrong")
    page.locator("#password").fill("wrong")
    page.locator("button[type='submit']").click()
    # Flash error has both .flash and .error classes
    expect(page.locator("#flash.error")).to_be_visible()

#-------- XPath ----------------------------------------------------
def test_xpath_button(page: Page):
    page.goto(f"{BASE}/login")
    page.locator("//*[@id='username']").fill("tomsmith")
    page.locator("//*[@id='password']").fill("SuperSecretPassword!")
    page.locator("//button[@type='submit']").click()
    expect(page.locator("//div[@id='flash']")).to_contain_text("secure area")

def test_xpath_checkboxes_by_positions(page: Page):
    page.goto(f"{BASE}/checkboxes")

    # XPath position() starts at 1 not 0
    first = page.locator("(//input[@type='checkbox'])[1]")
    second = page.locator("(//input[@type='checkbox'])[2]")
    expect(first).not_to_be_checked()
    expect(second).to_be_checked()

#-------- Handling multiple matches — .nth() .first .last .filter() ----------------------------

def test_nth_checkbox(page: Page):
    page.goto(f"{BASE}/checkboxes")
    checkboxes = page.locator("input[type='checkbox']")

    #Total count
    expect(checkboxes).to_have_count(2)

    # First is unchecked, second is checked
    expect(checkboxes.nth(0)).not_to_be_checked()
    expect(checkboxes.nth(1)).to_be_checked()

    # .first and .last are shorthand
    expect(checkboxes.first).not_to_be_checked()
    expect(checkboxes.last).to_be_checked()

def test_chained_locator(page: Page):
    page.goto(f"{BASE}/login")

    # Find the form first, then inputs inside it
    form = page.locator("form")
    form.locator("#username").fill("tomsmith")
    form.locator("#password").fill("SuperSecretPassword!")
    form.get_by_role("button", name="Login").click()
    expect(page.locator("#flash.success")).to_be_visible()