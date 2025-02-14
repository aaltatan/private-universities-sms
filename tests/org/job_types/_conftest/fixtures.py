import pytest
from django.contrib.auth.models import Permission
from django.db.models import Model
from django.urls import reverse

from apps.core.models import User
from apps.core.utils import Deleter
from apps.org.models import JobType
from tests.utils import reset_sequence


APP_LABEL = "org"
SUBAPP_LABEL = "job_types"
MODEL_NAME = "JobType"
OBJECT_NAME = "jobtype"


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
    return JobType


@pytest.fixture
def api_keys() -> list[str]:
    return ["id", "name", "description", "job_subtypes"]


@pytest.fixture
def index_columns() -> list[str]:
    return ["name", "description", "options"]


@pytest.fixture
def counts() -> dict[str, int]:
    return {
        "objects": 304,
        "bulk_delete_batch": 50,
    }


@pytest.fixture
def urls() -> dict[str, str]:
    return {
        "api": f"/api/{SUBAPP_LABEL.replace('_', '-')}/",
        "index": reverse(f"{SUBAPP_LABEL}:index"),
        "create": reverse(f"{SUBAPP_LABEL}:create"),
    }


@pytest.fixture
def templates() -> dict[str, str]:
    return {
        "index": f"apps/{SUBAPP_LABEL}/index.html",
        "create": f"apps/{SUBAPP_LABEL}/create.html",
        "update": f"apps/{SUBAPP_LABEL}/update.html",
        "table": f"components/{SUBAPP_LABEL}/table.html",
        "create_form": f"components/{SUBAPP_LABEL}/create.html",
        "update_form": f"components/{SUBAPP_LABEL}/update.html",
        "create_modal_form": f"components/{SUBAPP_LABEL}/modal-create.html",
        "update_modal_form": f"components/{SUBAPP_LABEL}/modal-update.html",
        "delete_modal": "components/blocks/modals/delete.html",
    }


@pytest.fixture
def clean_data_sample() -> dict[str, str]:
    return {
        "name": "محافظة دمشق",
        "description": "دمشق",
    }


@pytest.fixture(scope="package")
def custom_deleter():
    class CustomDeleter(Deleter[JobType]):
        error_obj_msg = "error obj message"
        error_qs_msg = "error qs message"

        def check_obj_deleting_possibility(self, obj: JobType) -> bool:
            return obj.pk not in [1, 2]

        def check_queryset_deleting_possibility(self, qs) -> bool:
            return not qs.filter(pk__in=[1, 2]).exists()

    return CustomDeleter


@pytest.fixture(scope="package", autouse=True)
def create_objects(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        job_types = [
            {"name": "محافظة حماه", "description": "goo"},
            {"name": "محافظة حمص", "description": "meta"},
            {"name": "محافظة ادلب", "description": "meta"},
            {"name": "محافظة المنيا", "description": "language mena"},
        ]

        for job_type in job_types:
            JobType.objects.create(**job_type)

        for idx in range(1, 301):
            string = str(idx).rjust(3, "0")
            JobType.objects.create(name=f"City {string}", description=string)
        yield
        JobType.objects.all().delete()
        reset_sequence(JobType)


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
