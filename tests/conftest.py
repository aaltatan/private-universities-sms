import pytest
from django.test import Client
from rest_framework.test import APIClient

from tests.utils import get_token_headers


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def headers_modal_GET() -> dict[str, str]:
    return {
        "modal": "true",
        "Hx-Request": "true",
    }


@pytest.fixture
def admin_headers(client: Client) -> dict[str, str]:
    return get_token_headers(client, admin=True)


@pytest.fixture
def user_headers(client: Client) -> dict[str, str]:
    return get_token_headers(client)
