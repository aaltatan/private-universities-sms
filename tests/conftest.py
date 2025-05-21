import pytest
from django.test import Client
from rest_framework.test import APIClient

from apps.core.constants import PERMISSION
from apps.core.models import Activity, User

from .utils import get_token_headers


@pytest.fixture(autouse=True)
def mock_per_page(settings) -> None:
    settings.PER_PAGE = 10


@pytest.fixture(
    scope="package",
    params=[
        (
            "add",
            (
                ("add_btn_exists", 1),
                ("delete_btn_exists", 0),
                ("delete_all_btn_exists", 0),
                ("edit_btn_exists", 0),
                ("export_btn_exists", 0),
                ("activities_btn_exists", 0),
            ),
        ),
        (
            "delete",
            (
                ("add_btn_exists", 0),
                ("delete_btn_exists", 1),
                ("delete_all_btn_exists", 1),
                ("edit_btn_exists", 0),
                ("export_btn_exists", 0),
                ("activities_btn_exists", 0),
            ),
        ),
        (
            "change",
            (
                ("add_btn_exists", 0),
                ("delete_btn_exists", 0),
                ("delete_all_btn_exists", 0),
                ("edit_btn_exists", 1),
                ("export_btn_exists", 0),
                ("activities_btn_exists", 0),
            ),
        ),
        (
            "export",
            (
                ("add_btn_exists", 0),
                ("delete_btn_exists", 0),
                ("delete_all_btn_exists", 0),
                ("edit_btn_exists", 0),
                ("export_btn_exists", 1),
                ("activities_btn_exists", 0),
            ),
        ),
        (
            "view_activity",
            (
                ("add_btn_exists", 0),
                ("delete_btn_exists", 0),
                ("delete_all_btn_exists", 0),
                ("edit_btn_exists", 0),
                ("export_btn_exists", 0),
                ("activities_btn_exists", 1),
            ),
        ),
    ],
)
def buttons_test_cases(
    request: pytest.FixtureRequest,
) -> tuple[PERMISSION, tuple[tuple[str, int], ...]]:
    return request.param


@pytest.fixture(scope="session")
def permissions() -> tuple[PERMISSION, ...]:
    return (
        "view",
        "add",
        "change",
        "delete",
        "export",
        "view_activity",
    )


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
        User.objects.create_superuser(
            username="admin",
            password="password",
        )
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
