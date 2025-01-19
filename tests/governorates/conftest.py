import pytest
from django.contrib.auth.models import Permission
from django.db.models import Model
from django.urls import reverse

from apps.core.models import User
from apps.governorates.models import Governorate
from tests.utils import create_base_users


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
        "table": f"components/{APP_LABEL}/table.html",
        "create_form": f"components/{APP_LABEL}/create.html",
        "update_form": f"components/{APP_LABEL}/update.html",
        "create_modal_form": f"components/{APP_LABEL}/modal-create.html",
        "update_modal_form": f"components/{APP_LABEL}/modal-update.html",
        "delete_modal": "components/blocks/modals/delete.html",
    }


@pytest.fixture
def clean_data_sample() -> dict[str, str]:
    return {
        "name": "محافظة دمشق",
        "description": "دمشق",
    }


@pytest.fixture(scope="package", autouse=True)
def objects(django_db_setup, django_db_blocker) -> None:
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


@pytest.fixture(autouse=True, scope="package")
def create_users(django_db_setup, django_db_blocker) -> None:
    with django_db_blocker.unblock():
        create_base_users()
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
