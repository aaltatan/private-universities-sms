import pytest
from django.urls import reverse
from django.test import Client
from selectolax.parser import HTMLParser

from tests.utils import is_template_used


@pytest.mark.django_db
def test_index_without_authentication_view(client: Client):
    response = client.get(reverse("core:index"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_index_authentication_view(client: Client):
    client.login(
        username="user_with_no_perm",
        password="password",
    )
    response = client.get(reverse("core:index"))

    assert response.status_code == 200
    assert is_template_used("apps/core/index.html", response)


@pytest.mark.django_db
def test_index_authentication_view_with_no_perm(client: Client):
    client.login(
        username="user_with_no_perm",
        password="password",
    )
    response = client.get(reverse("core:index"))
    parser = HTMLParser(response.content)

    aside = parser.css_first("nav[aria-label='sidebar navigation']")
    links = aside.css("div a")

    assert aside is not None
    assert len(links) == 1


@pytest.mark.django_db
def test_index_authentication_view_with_perm(admin_client: Client):
    response = admin_client.get(reverse("core:index"))
    parser = HTMLParser(response.content)
    aside = parser.css_first("nav[aria-label='sidebar navigation']")
    links = aside.css("div a")

    assert aside is not None
    assert len(links) > 1
