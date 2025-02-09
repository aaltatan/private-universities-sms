import pytest
import pytest_mock
from django.test import Client
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model

from tests.common import actions


@pytest.mark.django_db
def test_bulk_delete_modal_response(
    admin_client: Client,
    urls: dict[str, str],
    counts: dict[str, int],
):
    actions.test_bulk_delete_modal_response(admin_client, urls, counts)


@pytest.mark.django_db
def test_bulk_delete_without_permissions(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
    counts: dict[str, int],
):
    actions.test_bulk_delete_without_permissions(client, urls, subapp_label, counts)


@pytest.mark.django_db
def test_bulk_delete_with_permissions(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    actions.test_bulk_delete_with_permissions(admin_client, urls, model, counts)


@pytest.mark.django_db
def test_bulk_action_not_found(
    admin_client: Client,
    urls: dict[str, str],
    counts: dict[str, int],
):
    actions.test_bulk_action_not_found(admin_client, urls, counts)


@pytest.mark.django_db
def test_bulk_delete_with_permissions_only_for_view(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
    counts: dict[str, int],
):
    actions.test_bulk_delete_with_permissions_only_for_view(
        client, urls, subapp_label, counts
    )


@pytest.mark.django_db
def test_bulk_delete_when_no_deleter_class_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
    counts: dict[str, int],
):
    actions.test_bulk_delete_when_no_deleter_class_is_defined(
        admin_client, urls, mocker, app_label, subapp_label, counts
    )


@pytest.mark.django_db
def test_bulk_delete_when_deleter_class_is_not_subclass_of_Deleter(
    admin_client: Client,
    urls: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
    counts: dict[str, int],
):
    actions.test_bulk_delete_when_deleter_class_is_not_subclass_of_Deleter(
        admin_client, urls, mocker, app_label, subapp_label, counts
    )


@pytest.mark.django_db
def test_bulk_delete_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    actions.test_bulk_delete_objects(api_client, urls, admin_headers, model, counts)
