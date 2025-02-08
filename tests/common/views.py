from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.constants import PERMISSION
from tests.utils import is_template_used, parse_buttons


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


def test_view_index_file(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    response = admin_client.get(urls["index"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)


def test_view_has_all_html_elements_which_need_permissions(
    admin_client: Client, urls: dict[str, str]
):
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert buttons["add_btn_exists"]
    assert buttons["export_btn_exists"]
    assert buttons["activities_btn_exists"]
    assert buttons["delete_btn_exists"]
    assert buttons["edit_btn_exists"]
    assert buttons["delete_all_btn_exists"]
    assert buttons["activities_btn_exists"]


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


def test_view_buttons_does_exists(
    client: Client,
    urls: dict[str, str],
    subapp_label: str,
    buttons_test_cases: tuple[PERMISSION, tuple[tuple[str, int], ...]],
):
    perm, buttons = buttons_test_cases
    client.login(
        username=f"{subapp_label}_user_with_view_{perm}_perm",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    res_buttons = parse_buttons(parser)

    assert response.status_code == status.HTTP_200_OK
    for key, exists in buttons:
        exists = bool(exists)
        assert res_buttons[key] is exists


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


def test_read_objects_without_permissions(
    api_client: APIClient, urls: dict[str, str], user_headers: dict[str, str]
):
    response: Response = api_client.get(
        path=urls["api"],
        headers=user_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_object(
    api_client: APIClient, urls: dict[str, str], admin_headers: dict[str, str]
):
    response: Response = api_client.get(
        path=f"{urls['api']}1/",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK


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
