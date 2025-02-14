import pytest
from django.contrib.auth.models import Permission
from django.db.models import Model
from django.urls import reverse

from apps.core.models import User
from apps.geo.models import Governorate, City
from apps.core.utils import Deleter
from tests.utils import reset_sequence

from .factories import GovernorateFactory, CityFactory


APP_LABEL = "geo"
SUBAPP_LABEL = "cities"
MODEL_NAME = "City"
OBJECT_NAME = "city"


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
    return City


@pytest.fixture
def governorate_model() -> Governorate:
    return Governorate


@pytest.fixture
def api_keys() -> list[str]:
    return ["id", "name", "description", "governorate"]


@pytest.fixture
def index_columns() -> list[str]:
    return ["name", "description", "governorate", "options"]


@pytest.fixture
def counts() -> dict[str, int]:
    return {
        "objects": 101,
        "bulk_delete_batch": 50,
    }


@pytest.fixture
def urls() -> dict[str, str]:
    return {
        "api": f"/api/{SUBAPP_LABEL}/",
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
        "name": "مدينة حماه",
        "governorate": "محافظة حماه",
        "description": "حماه",
    }


@pytest.fixture(scope="package")
def custom_deleter():
    class CustomDeleter(Deleter[City]):
        error_obj_msg = "error obj message"
        error_qs_msg = "error qs message"

        def check_obj_deleting_possibility(self, obj: City) -> bool:
            return False

        def check_queryset_deleting_possibility(self, qs: City) -> bool:
            return False

    return CustomDeleter


@pytest.fixture(scope="package", autouse=True)
def create_objects(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        governorates = GovernorateFactory.create_batch(10)

        for gov in governorates:
            CityFactory.create_batch(10, governorate=gov)

        CityFactory.create(name="Hama City", governorate=governorates[0])

        yield

        City.objects.all().delete()
        Governorate.objects.all().delete()

        reset_sequence(Governorate)
        reset_sequence(City)


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
            perm = Permission.objects.get(codename=f"{p}_{OBJECT_NAME}")
            user = User.objects.create_user(
                username=f"{SUBAPP_LABEL}_user_with_view_{p}_perm",
                password="password",
            )
            user.user_permissions.add(view_perm, perm)
