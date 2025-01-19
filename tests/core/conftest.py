from typing import Any, Generator

import pytest
from playwright.sync_api import Page, sync_playwright

from tests.utils import create_base_users


@pytest.fixture
def admin_page(db, live_server) -> Generator[Page, Any, None]:
    """Get authenticated page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=50)
        page = browser.new_page()
        page.goto(live_server.url)
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "admin")
        page.click("button[type='submit']")
        page.wait_for_selector('nav[aria-label="sidebar navigation"]')
        yield page


@pytest.fixture(autouse=True, scope="package")
def create_users(django_db_setup, django_db_blocker) -> None:
    with django_db_blocker.unblock():
        create_base_users()
