import pytest
import pytest_mock
from django.test import Client
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model

from tests.common import delete


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_delete_perm(
    admin_client: Client, urls: dict[str, str]
) -> None:
    delete.test_delete_btn_appearance_if_user_has_delete_perm(admin_client, urls)


@pytest.mark.django_db
def test_delete_object_if_headers_has_no_hx_request(
    admin_client: Client, model: type[Model]
) -> None:
    delete.test_delete_object_if_headers_has_no_hx_request(admin_client, model)


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_no_delete_perm(
    client: Client,
    urls: dict[str, str],
    model: type[Model],
    subapp_label: str,
) -> None:
    delete.test_delete_btn_appearance_if_user_has_no_delete_perm(
        client, urls, model, subapp_label
    )


@pytest.mark.django_db
def test_get_delete_modal_without_using_htmx(
    model: type[Model], admin_client: Client
) -> None:
    delete.test_get_delete_modal_without_using_htmx(model, admin_client)


@pytest.mark.django_db
def test_get_delete_modal_with_using_htmx(
    model: type[Model],
    admin_client: Client,
    templates: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    delete.test_get_delete_modal_with_using_htmx(
        model, admin_client, templates, headers_modal_GET
    )


@pytest.mark.django_db
def test_delete_object(
    model: type[Model],
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    counts: dict[str, int],
) -> None:
    delete.test_delete_object(model, admin_client, urls, headers_modal_GET, counts)


@pytest.mark.django_db
def test_delete_when_no_deleter_class_is_defined(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    delete.test_delete_when_no_deleter_class_is_defined(
        admin_client, model, headers_modal_GET, mocker, app_label, subapp_label
    )


@pytest.mark.django_db
def test_delete_when_deleter_class_is_not_subclass_of_Deleter(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    delete.test_delete_when_deleter_class_is_not_subclass_of_Deleter(
        admin_client, model, headers_modal_GET, mocker, app_label, subapp_label
    )


@pytest.mark.django_db
def test_api_delete_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    delete.test_api_delete_object(api_client, urls, admin_headers, model, counts)


@pytest.mark.django_db
def test_delete_object_with_invalid_id(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    model_name: str,
    counts: dict[str, int],
):
    delete.test_delete_object_with_invalid_id(
        api_client, urls, admin_headers, model, model_name, counts
    )


@pytest.mark.django_db
def test_delete_and_bulk_delete_object_when_deleter_class_is_None(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    delete.test_delete_and_bulk_delete_object_when_deleter_class_is_None(
        api_client, urls, admin_headers, mocker, app_label, subapp_label
    )


@pytest.mark.django_db
def test_delete_and_bulk_delete_object_when_deleter_class_is_not_a_subclass_of_Deleter(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    delete.test_delete_and_bulk_delete_object_when_deleter_class_is_not_a_subclass_of_Deleter(
        api_client, urls, admin_headers, mocker, app_label, subapp_label
    )
