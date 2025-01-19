import pytest

from tests.utils import create_base_users


@pytest.fixture(autouse=True, scope="package")
def create_users(django_db_setup, django_db_blocker) -> None:
    with django_db_blocker.unblock():
        create_base_users()
