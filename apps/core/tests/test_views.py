import pytest
from django.urls import reverse
from django.test import Client

from ..models import User


@pytest.fixture(autouse=True)
def create_users() -> None:
    User.objects.create_user(username="test", password="test")


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
