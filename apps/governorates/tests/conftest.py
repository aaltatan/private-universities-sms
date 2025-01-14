import pytest
from django.db.models import Model
from django.test import Client
from django.contrib.auth.models import Permission
from django.urls import reverse

from apps.core.models import User

from ..models import Governorate


APP_LABEL = "governorates"


@pytest.fixture
def filename() -> str:
    return APP_LABEL.title()


@pytest.fixture
def model() -> type[Model]:
    return Governorate


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def super_client() -> Client:
    client = Client()
    client.login(username="admin", password="admin")
    return client


@pytest.fixture
def urls() -> dict[str, str]:
    return {
        "index": reverse(f"{APP_LABEL}:index"),
        "create": reverse(f"{APP_LABEL}:create"),
    }


@pytest.fixture
def templates() -> dict[str, str]:
    return {
        "index": f"apps/{APP_LABEL}/index.html",
        "create": f"apps/{APP_LABEL}/create.html",
        "create_form": "components/forms/create.html",
        "create_modal_form": "components/app-forms/modal-create.html",
        "delete_modal": "components/blocks/modals/delete.html",
    }


@pytest.fixture
def headers_modal_GET() -> dict[str, str]:
    return {
        "modal": "true",
        "Hx-Request": "true",
    }


@pytest.fixture
def clean_data_sample() -> dict[str, str]:
    return {
        "name": "محافظة دمشق",
        "description": "دمشق",
    }


@pytest.fixture(autouse=True)
def governorates() -> None:
    governorates = [
        {"name": "محافظة حماه", "description": "حماه"},
        {"name": "محافظة حمص", "description": "حمص"},
        {"name": "محافظة ادلب", "description": "ادلب"},
        {"name": "محافظة المنيا", "description": "المنيا"},
    ]

    for governorate in governorates:
        Governorate.objects.create(**governorate)


@pytest.fixture
def dirty_data() -> list[dict]:
    return [
        {
            "data": {
                "name": "Ha",
                "description": "google",
            },
            "error": "the field must be at least 4 characters long",
            "api_error": ["Ensure this field has at least 4 characters."],
        },
        {
            "data": {
                "name": "",
                "description": "",
            },
            "error": "This field is required.",
            "api_error": ["This field may not be blank."],
        },
        {
            "data": {
                "name": "a" * 265,
                "description": "",
            },
            "error": "Ensure this value has at most 255 characters (it has 265).",
            "api_error": ["Ensure this field has no more than 255 characters."],
        },
        {
            "data": {
                "name": "محافظة حماه",
                "description": "google",
            },
            "error": "Governorate with this Name already exists.",
            "api_error": ["governorate with this name already exists."],
        },
    ]


@pytest.fixture(autouse=True)
def create_users() -> None:
    User.objects.create_superuser(
        username="admin",
        password="admin",
    )

    user_with_view_perm_only = User.objects.create_user(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )

    view_perm = Permission.objects.get(codename="view_governorate")

    user_with_view_perm_only.user_permissions.add(view_perm)
