import pytest
from django.test import Client
from rest_framework.test import APIClient

from apps.core.models import Activity, User
from tests.utils import get_token_headers


@pytest.fixture(scope="session")
def activity_model() -> Activity:
    return Activity


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def headers_modal_GET() -> dict[str, str]:
    return {
        "modal": "true",
        "Hx-Request": "true",
    }


@pytest.fixture(autouse=True, scope="session")
def create_base_users(django_db_setup, django_db_blocker) -> None:
    with django_db_blocker.unblock():
        User.objects.create_user(
            username="user_with_no_perm",
            password="password",
        )


@pytest.fixture
def admin_headers(client: Client, admin_user) -> dict[str, str]:
    return get_token_headers(client, admin=True)


@pytest.fixture
def user_headers(client: Client) -> dict[str, str]:
    return get_token_headers(client)
