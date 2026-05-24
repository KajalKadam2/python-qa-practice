# Complete assertion reference — all in one file

from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"

def test_all_assertions(page: Page):
    page.goto(f"{BASE}/login")

    # ── Page assertions ───────────────────────────
    expect(page).to_have_url(f"{BASE}/login")
    expect(page).to_have_title("The Internet")

    # ── Visibility ────────────────────────────────
    expect(page.get_by_label("Username")).to_be_visible()
    expect(page.locator("#flash")).to_be_hidden()

    # ── State ─────────────────────────────────────
    expect(page.get_by_label("Username")).to_be_enabled()
    expect(page.get_by_label("Username")).to_be_editable()

    # ── Fill and assert value ─────────────────────
    page.get_by_label("Username").fill("tomsmith")
    expect(page.get_by_label("Username")).to_have_value("tomsmith")

    # ── Attribute ─────────────────────────────────
    expect(page.locator("#password")).to_have_attribute("type", "password")

    # ── Login and assert result ───────────────────
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(f"{BASE}/secure")
    expect(page.locator("#flash.success")).to_be_visible()
    expect(page.locator("#flash.success")).to_contain_text("secure area")

def test_checkboxes_assertions(page: Page):
    page.goto(f"{BASE}/checkboxes")
    checkboxes = page.locator("input[type='checkbox']")

    # ── Count ─────────────────────────────────────
    expect(checkboxes).to_have_count(2)

    # ── Checked state ─────────────────────────────
    expect(checkboxes.first).not_to_be_checked()
    expect(checkboxes.last).to_be_checked()

    # ── After action ──────────────────────────────
    checkboxes.first.check()
    expect(checkboxes.first).to_be_checked()