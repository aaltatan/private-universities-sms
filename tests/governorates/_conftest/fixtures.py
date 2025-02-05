import pytest
from django.contrib.auth.models import Permission
from django.db.models import Model
from django.urls import reverse

from apps.core.models import User
from apps.governorates.models import Governorate
from tests.utils import reset_sequence


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
def counts() -> dict[str, int]:
    return {
        "objects": 304,
        "bulk_delete_batch": 50,
    }


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
def create_objects(django_db_setup, django_db_blocker):
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
            string = str(idx).rjust(3, "0")
            Governorate.objects.create(
                name=f"City {string}",
                description=string,
            )
        yield
        Governorate.objects.all().delete()
        reset_sequence(Governorate)


@pytest.fixture(autouse=True, scope="package")
def create_users(django_db_setup, django_db_blocker) -> None:
    with django_db_blocker.unblock():
        user_with_view_perm_only = User.objects.create_user(
            username=f"{APP_LABEL}_user_with_view_perm_only",
            password="password",
        )
        view_perm = Permission.objects.get(codename="view_governorate")
        user_with_view_perm_only.user_permissions.add(view_perm)

        perms = ["add", "change", "delete", "export"]

        for p in perms:
            perm = Permission.objects.get(
                codename=f"{p}_governorate",
            )
            user = User.objects.create_user(
                username=f"{APP_LABEL}_user_with_view_{p}_perm",
                password="password",
            )
            user.user_permissions.add(view_perm, perm)
