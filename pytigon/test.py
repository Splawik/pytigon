from playwright.sync_api import Playwright, sync_playwright, expect
import os


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pytigon.eu/")
    page.get_by_role("link", name="").click()
    page.locator("#username_").fill("auto")
    page.get_by_label("Password").fill("anawa")
    page.get_by_role("button", name="OK").click()
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
