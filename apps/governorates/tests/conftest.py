import pytest
from django.contrib.auth.models import Permission
from django.db.models import Model
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient

from apps.core.models import User

from ..models import Governorate


APP_LABEL = "governorates"
MODEL_NAME = "Governorate"


@pytest.fixture
def filename() -> str:
    return APP_LABEL.title()


@pytest.fixture
def model_name() -> str:
    return MODEL_NAME


@pytest.fixture
def app_label() -> str:
    return APP_LABEL


@pytest.fixture
def model() -> type[Model]:
    return Governorate


@pytest.fixture
def admin_headers() -> dict[str, str]:
    client = Client()
    response = client.post(
        "/api/token/",
        {"username": "admin", "password": "admin"},
    )
    admin_token = response.json()["access"]
    return {
        "Authorization": f"Bearer {admin_token}",
    }


@pytest.fixture
def user_headers() -> dict[str, str]:
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


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


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
        "api": f"/api/{APP_LABEL}/",
        "index": reverse(f"{APP_LABEL}:index"),
        "create": reverse(f"{APP_LABEL}:create"),
    }


@pytest.fixture
def templates() -> dict[str, str]:
    return {
        "index": f"apps/{APP_LABEL}/index.html",
        "create": f"apps/{APP_LABEL}/create.html",
        "update": f"apps/{APP_LABEL}/update.html",
        "create_form": "components/app-forms/create.html",
        "update_form": "components/app-forms/update.html",
        "create_modal_form": "components/app-forms/modal-create.html",
        "update_modal_form": "components/app-forms/modal-update.html",
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


@pytest.fixture(scope="session", autouse=True)
def objects(django_db_setup, django_db_blocker):
    del django_db_setup
    with django_db_blocker.unblock():
        governorates = [
            {"name": "محافظة حماه", "description": "goo"},
            {"name": "محافظة حمص", "description": "meta"},
            {"name": "محافظة ادلب", "description": "meta"},
            {"name": "محافظة المنيا", "description": "language mena"},
        ]

        for governorate in governorates:
            Governorate.objects.create(**governorate)

        for idx in range(1, 301):
            description_order = str(abs(idx - 301)).rjust(3, "0")
            Governorate.objects.create(
                name=f"City {idx}",
                description=description_order,
            )
        yield


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

    User.objects.create_user(
        username="user_with_no_perm",
        password="user_with_no_perm",
    )
    user_with_view_perm_only = User.objects.create_user(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )
    view_perm = Permission.objects.get(codename="view_governorate")
    user_with_view_perm_only.user_permissions.add(view_perm)

    perms = ["add", "change", "delete", "export"]

    for p in perms:
        perm = Permission.objects.get(
            codename=f"{p}_governorate",
        )
        user = User.objects.create_user(
            username=f"user_with_view_{p}_perm",
            password=f"user_with_view_{p}_perm",
        )
        user.user_permissions.add(view_perm, perm)
