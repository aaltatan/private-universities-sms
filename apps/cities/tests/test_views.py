import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from apps.core.tests.utils import parse_buttons


@pytest.mark.django_db
def test_index_has_checkboxes_admin(
    super_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    response = super_client.get(urls["index"])
    parser = HTMLParser(response.content)
    checkboxes = parser.css("input[id^='row-check-']")

    assert len(checkboxes) == 10
    assert response.status_code == 200
    assert templates["index"] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_index_has_checkboxes_with_view_delete_perms(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    client.login(
        username="user_with_view_delete_perm",
        password="user_with_view_delete_perm",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    checkboxes = parser.css("input[id^='row-check-']")

    assert response.status_code == 200
    assert len(checkboxes) == 10
    assert templates["index"] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_index_has_checkboxes_with_no_permission(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    checkboxes = parser.css("input[id^='row-check-']")

    assert len(checkboxes) == 0
    assert response.status_code == 200
    assert templates["index"] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_view_index_file(
    super_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    response = super_client.get(urls["index"])

    assert response.status_code == 200
    assert templates["index"] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_view_has_all_html_elements_which_need_permissions(
    super_client: Client, urls: dict[str, str]
):
    response = super_client.get(urls["index"])
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
def test_view_contains_objects(
    super_client: Client,
    urls: dict[str, str],
):
    response = super_client.get(urls["index"])

    assert "City 1" in response.content.decode()
    assert "City 2" in response.content.decode()
    assert "City 3" in response.content.decode()

    assert "حماه" in response.content.decode()
    assert "حمص" in response.content.decode()
    assert "ادلب" in response.content.decode()


@pytest.mark.django_db
def test_view_user_has_no_permissions(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_no_perm",
        password="user_with_no_perm",
    )

    response = client.get(urls["index"])
    assert response.status_code == 403


@pytest.mark.django_db
def test_view_user_has_view_permissions(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )

    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == 200
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_add(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_add_perm",
        password="user_with_view_add_perm",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == 200
    assert buttons["add_btn_exists"] is True
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_change(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_change_perm",
        password="user_with_view_change_perm",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == 200
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is True
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_delete(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_delete_perm",
        password="user_with_view_delete_perm",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == 200
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is True
    assert buttons["delete_all_btn_exists"] is True
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is False


@pytest.mark.django_db
def test_view_user_has_view_permissions_export(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_export_perm",
        password="user_with_view_export_perm",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    buttons = parse_buttons(parser)

    assert response.status_code == 200
    assert buttons["add_btn_exists"] is False
    assert buttons["delete_btn_exists"] is False
    assert buttons["delete_all_btn_exists"] is False
    assert buttons["edit_btn_exists"] is False
    assert buttons["export_btn_exists"] is True
