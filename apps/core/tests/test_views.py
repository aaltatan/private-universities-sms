import pytest
from django.urls import reverse
from django.test import Client
from selectolax.parser import HTMLParser

from ..models import User


@pytest.fixture(autouse=True)
def create_users() -> None:
    User.objects.create_user(username="test", password="test")
    User.objects.create_superuser(
        username="admin",
        password="admin",
    )


@pytest.fixture()
def client() -> Client:
    return Client()


@pytest.mark.django_db
def test_index_without_authentication_view(client: Client):
    response = client.get(reverse("core:index"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_index_authentication_view(client: Client):
    client.login(username="test", password="test")
    response = client.get(reverse("core:index"))

    assert response.status_code == 200
    assert "apps/core/index.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_index_authentication_view_with_no_perm(client: Client):
    client.login(username="test", password="test")
    response = client.get(reverse("core:index"))
    parser = HTMLParser(response.content)

    aside = parser.css_first("nav[aria-label='sidebar navigation']")
    links = aside.css("div a")

    assert aside is not None
    assert len(links) == 1


@pytest.mark.django_db
def test_index_authentication_view_with_perm(client: Client):
    client.login(username="admin", password="admin")
    response = client.get(reverse("core:index"))
    parser = HTMLParser(response.content)
    aside = parser.css_first("nav[aria-label='sidebar navigation']")
    links = aside.css("div a")

    assert aside is not None
    assert len(links) == 2
