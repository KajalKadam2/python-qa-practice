# XPATH


from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

def test_xpath_by_text(page: Page):
    page.goto(f"{BASE}/login")

    #XPath to find element containing specific text
    label = page.locator("//label[contains(text(), 'Username')]")
    expect(label).to_be_visible()

def text_xpath_by_attribute(page: Page):
    page.goto(f"{BASE}/login")
    
    #XPath by attribute value
    username = page.locator("//input[@id='username']")
    username.fill("tomsmith")
    expect(username).to_have_value("tomsmith")

def test_xpath_parent_child(page: Page):
    page.goto(f"{BASE}/checkboxes")

    #XPath: find form, then get checkboxes inside it
    checkboxes = page.locator("//form[@id='checkboxes']//input")
    expect(checkboxes).to_have_count(2)