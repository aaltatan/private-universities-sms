import pytest
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from tests.utils import is_template_used, parse_buttons


@pytest.mark.django_db
def test_index_GET_with_htmx(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    headers = {
        "HX-Request": "true",
    }
    response = admin_client.get(urls["index"], headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["table"], response)


@pytest.mark.django_db
def test_index_has_checkboxes_admin(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    checkboxes = parser.css("input[id^='row-check-']")

    assert len(checkboxes) == 10
    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)


@pytest.mark.django_db
def test_index_has_checkboxes_with_view_delete_perms(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_delete_perm",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    checkboxes = parser.css("input[id^='row-check-']")

    assert response.status_code == status.HTTP_200_OK
    assert len(checkboxes) == 10
    assert is_template_used(templates["index"], response)


@pytest.mark.django_db
def test_index_has_checkboxes_with_no_permission(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_perm_only",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    checkboxes = parser.css("input[id^='row-check-']")

    assert len(checkboxes) == 0
    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)


@pytest.mark.django_db
def test_view_index_file(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    response = admin_client.get(urls["index"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)


@pytest.mark.django_db
def test_view_has_all_html_elements_which_need_permissions(
    admin_client: Client, urls: dict[str, str]
):
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)

    add_new_btn = parser.css_first(
        "[aria-label='create new object']",
    )
    export_btn = parser.css_first("a[aria-label^='export table']")
    row_delete_btn = parser.css_first(
        "a[aria-label='delete object']",
    )
    row_edit_btn = parser.css_first("a[aria-label='edit object']")
    row_delete_all_btn = parser.css_first(
        "input[aria-label='delete all objects']",
    )

    assert add_new_btn is not None
    assert export_btn is not None
    assert row_delete_btn is not None
    assert row_edit_btn is not None
    assert row_delete_all_btn is not None


@pytest.mark.django_db
def test_view_user_has_no_permissions(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_no_perm",
        password="password",
    )

    response = client.get(urls["index"])
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_view_user_has_view_permissions(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_perm_only",
        password="password",
    )

    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == status.HTTP_200_OK
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_add(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_add_perm",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == status.HTTP_200_OK
    assert buttons["add_btn_exists"]
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_change(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_change_perm",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == status.HTTP_200_OK
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"]
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_delete(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_delete_perm",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == status.HTTP_200_OK
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"]
    assert buttons["delete_all_btn_exists"]
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_export(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_export_perm",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == status.HTTP_200_OK
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"]


@pytest.mark.django_db
def test_read_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    counts: dict[str, int],
):
    response: Response = api_client.get(
        path=urls["api"],
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == counts["objects"]
    assert len(response.json()["results"]) == 10


@pytest.mark.django_db
def test_read_objects_without_permissions(
    api_client: APIClient, urls: dict[str, str], user_headers: dict[str, str]
):
    response: Response = api_client.get(
        path=urls["api"],
        headers=user_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_read_object(
    api_client: APIClient, urls: dict[str, str], admin_headers: dict[str, str]
):
    response: Response = api_client.get(
        path=f"{urls['api']}1/",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_read_object_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f"{urls['api']}1/",
        headers=user_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_read_object_with_invalid_id(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f"{urls['api']}4123/",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
