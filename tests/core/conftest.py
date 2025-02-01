from typing import Any, Generator

import pytest
from django.urls import reverse
from playwright.sync_api import Page, sync_playwright

from apps.governorates.models import Governorate
from tests.utils import reset_sequence


@pytest.fixture
def model() -> Governorate:
    return Governorate


@pytest.fixture
def urls() -> dict[str, str]:
    return {
        "api": "/api/governorates/",
        "autocomplete": reverse("core:autocomplete"),
        "index": reverse("governorates:index"),
        "create": reverse("governorates:create"),
    }


@pytest.fixture
def templates() -> dict[str, str]:
    return {
        "autocomplete-item": "widgets/autocomplete-item.html",
        "activities": "apps/core/activities.html",
    }


@pytest.fixture(scope="package", autouse=True)
def create_governorates(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        governorates = [
            {"name": "محافظة حماه", "description": "goo"},
            {"name": "محافظة حمص", "description": "meta"},
            {"name": "محافظة ادلب", "description": "meta"},
            {"name": "محافظة المنيا", "description": "language mena"},
        ]
        for governorate in governorates:
            Governorate.objects.create(**governorate)
        yield
        Governorate.objects.all().delete()
        reset_sequence(Governorate)


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
