import pytest
from playwright.sync_api import Page


@pytest.mark.django_db
@pytest.mark.order("last")
def test_dark_mode(admin_page: Page):
    """Test dark mode."""
    expression = "document.documentElement.classList.contains('dark')"

    is_dark: bool = admin_page.evaluate(expression)
    admin_page.click('button[aria-label="toggle dark mode"]')
    is_light: bool = admin_page.evaluate(expression)

    assert is_dark is True
    assert is_light is False
