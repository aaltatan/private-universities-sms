import pytest
from django.test import Client
from rest_framework.test import APIClient

from apps.core.models import User


@pytest.fixture(autouse=True, scope="session")
def create_users(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create_user(
            username="user_with_no_perm",
            password="user_with_no_perm",
        )
        User.objects.create_superuser(
            username="admin",
            password="admin",
        )
        yield


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def admin_headers() -> Client:
    client = Client()
    response = client.post(
        "/api/token/",
        {"username": "admin", "password": "admin"},
    )
    admin_token = response.json()["access"]
    return {
        "Authorization": f"Bearer {admin_token}",
    }


@pytest.fixture(scope="session")
def user_headers() -> Client:
    client = Client()
    response = client.post(
        "/api/token/",
        {
            "username": "user_with_no_perm",
            "password": "user_with_no_perm",
        },
    )
    user_token = response.json()["access"]
    return {
        "Authorization": f"Bearer {user_token}",
    }


@pytest.fixture(scope="session")
def headers_modal_GET() -> dict[str, str]:
    return {
        "modal": "true",
        "Hx-Request": "true",
    }
