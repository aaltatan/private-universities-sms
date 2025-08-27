import pytest
from django.contrib.auth.models import Permission
from django.db import connection
from django.db.models import Model
from django.urls import reverse

from apps.core.models import User
from apps.core.utils import Deleter
from apps.org.models import Status
from tests.utils import reset_sequence

from .factories import StatusFactory

APP_LABEL = "org"
SUBAPP_LABEL = "statuses"
MODEL_NAME = "Status"
OBJECT_NAME = "status"


@pytest.fixture
def filename() -> str:
    return SUBAPP_LABEL.title()


@pytest.fixture
def model_name() -> str:
    return MODEL_NAME


@pytest.fixture
def app_label() -> str:
    return APP_LABEL


@pytest.fixture
def subapp_label() -> str:
    return SUBAPP_LABEL


@pytest.fixture
def model() -> type[Model]:
    return Status


@pytest.fixture
def api_keys() -> list[str]:
    return ["id", "name", "is_payable", "description"]


@pytest.fixture
def index_columns() -> list[str]:
    return [
        "name",
        "is payable",
        "is separated",
        "employees count",
        "description",
        "options",
    ]


@pytest.fixture
def counts() -> dict[str, int]:
    return {
        "objects": 100,
        "bulk_delete_batch": 50,
    }


@pytest.fixture
def urls() -> dict[str, str]:
    return {
        "api": f"/api/{APP_LABEL}/{SUBAPP_LABEL}/",
        "index": reverse(f"{APP_LABEL}:{SUBAPP_LABEL}:index"),
        "create": reverse(f"{APP_LABEL}:{SUBAPP_LABEL}:create"),
    }


@pytest.fixture
def templates() -> dict[str, str]:
    return {
        "index": f"apps/{APP_LABEL}/{SUBAPP_LABEL}/index.html",
        "create": f"apps/{APP_LABEL}/{SUBAPP_LABEL}/create.html",
        "update": f"apps/{APP_LABEL}/{SUBAPP_LABEL}/update.html",
        "table": f"components/{APP_LABEL}/{SUBAPP_LABEL}/table.html",
        "create_form": f"components/{APP_LABEL}/{SUBAPP_LABEL}/create.html",
        "update_form": f"components/{APP_LABEL}/{SUBAPP_LABEL}/update.html",
        "create_modal_form": f"components/{APP_LABEL}/{SUBAPP_LABEL}/modal-create.html",
        "update_modal_form": f"components/{APP_LABEL}/{SUBAPP_LABEL}/modal-update.html",
        "delete_modal": "components/blocks/modals/delete.html",
    }


@pytest.fixture
def clean_data_sample() -> dict[str, str]:
    return {
        "name": "معلق",
        "is_payable": True,
        "is_separated": False,
        "description": "دمشق",
    }


@pytest.fixture(scope="package")
def custom_deleter():
    class CustomDeleter(Deleter[Status]):
        error_obj_msg = "error obj message"
        error_qs_msg = "error qs message"

        def check_obj_executing_possibility(self, obj: Status) -> bool:
            return obj.pk not in [1, 2]

        def check_queryset_executing_possibility(self, qs) -> bool:
            return not qs.filter(pk__in=[1, 2]).exists()

    return CustomDeleter


@pytest.fixture(scope="package", autouse=True)
def create_objects(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        StatusFactory.create_batch(100)
        yield
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM org_status;")
        reset_sequence(Status)


@pytest.fixture(autouse=True, scope="package")
def create_users(django_db_setup, django_db_blocker, permissions) -> None:
    with django_db_blocker.unblock():
        user_with_view_perm_only = User.objects.create_user(
            username=f"{SUBAPP_LABEL}_user_with_view_perm_only",
            password="password",
        )
        view_perm = Permission.objects.get(codename=f"view_{OBJECT_NAME}")
        user_with_view_perm_only.user_permissions.add(view_perm)

        for p in permissions:
            perm = Permission.objects.get(
                codename=f"{p}_{OBJECT_NAME}",
            )
            user = User.objects.create_user(
                username=f"{SUBAPP_LABEL}_user_with_view_{p}_perm",
                password="password",
            )
            user.user_permissions.add(view_perm, perm)
