import pytest
from django.test import Client
from rest_framework.test import APIClient

from apps.core.constants import PERMISSION
from tests.common import views


@pytest.mark.django_db
def test_read_object_has_keys(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    api_keys: list[str],
):
    views.test_read_object_has_keys(api_client, urls, admin_headers, api_keys)


@pytest.mark.django_db
def test_index_has_right_columns(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    index_columns: list[str],
):
    views.test_index_has_right_columns(admin_client, urls, templates, index_columns)


@pytest.mark.django_db
def test_index_GET_with_htmx(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    views.test_index_GET_with_htmx(admin_client, urls, templates)


@pytest.mark.django_db
def test_index_has_checkboxes_admin(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    views.test_index_has_checkboxes_admin(admin_client, urls, templates)


@pytest.mark.django_db
def test_index_has_checkboxes_with_view_delete_perms(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
):
    views.test_index_has_checkboxes_with_view_delete_perms(
        client, urls, templates, subapp_label
    )


@pytest.mark.django_db
def test_index_has_checkboxes_with_no_permission(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
):
    views.test_index_has_checkboxes_with_no_permission(
        client, urls, templates, subapp_label
    )


@pytest.mark.django_db
def test_view_index_file(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    views.test_view_index_file(admin_client, urls, templates)


@pytest.mark.django_db
def test_view_has_all_html_elements_which_need_permissions(
    admin_client: Client, urls: dict[str, str]
):
    views.test_view_has_all_html_elements_which_need_permissions(admin_client, urls)


@pytest.mark.django_db
def test_view_user_has_no_permissions(client: Client, urls: dict[str, str]):
    views.test_view_user_has_no_permissions(client, urls)


@pytest.mark.django_db
def test_view_user_has_view_permissions(
    client: Client, urls: dict[str, str], subapp_label: str
):
    views.test_view_user_has_view_permissions(client, urls, subapp_label)


@pytest.mark.django_db
def test_view_buttons_does_exists(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
    buttons_test_cases: tuple[PERMISSION, tuple[tuple[str, int], ...]],
):
    views.test_view_buttons_does_exists(client, urls, subapp_label, buttons_test_cases)


@pytest.mark.django_db
def test_read_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    counts: dict[str, int],
):
    views.test_read_objects(api_client, urls, admin_headers, counts)


@pytest.mark.django_db
def test_read_objects_without_permissions(
    api_client: APIClient, urls: dict[str, str], user_headers: dict[str, str]
):
    views.test_read_objects_without_permissions(api_client, urls, user_headers)


@pytest.mark.django_db
def test_read_object(
    api_client: APIClient, urls: dict[str, str], admin_headers: dict[str, str]
):
    views.test_read_object(api_client, urls, admin_headers)


@pytest.mark.django_db
def test_read_object_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    views.test_read_object_without_permissions(api_client, urls, user_headers)


@pytest.mark.django_db
def test_read_object_with_invalid_id(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    views.test_read_object_with_invalid_id(api_client, urls, admin_headers)
