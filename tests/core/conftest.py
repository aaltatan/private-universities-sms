from typing import Any, Generator

from django.urls import reverse
import pytest
from playwright.sync_api import Page, sync_playwright

from tests.utils import create_base_users
from apps.governorates.models import Governorate


@pytest.fixture
def autocomplete_url() -> str:
    return reverse("core:autocomplete")


@pytest.fixture
def autocomplete_template() -> str:
    return "apps/core/autocomplete-item.html"


@pytest.fixture
def create_governorates(db) -> None:
    governorates = [
        {"name": "محافظة حماه", "description": "goo"},
        {"name": "محافظة حمص", "description": "meta"},
        {"name": "محافظة ادلب", "description": "meta"},
        {"name": "محافظة المنيا", "description": "language mena"},
    ]
    for governorate in governorates:
        Governorate.objects.create(**governorate)


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
