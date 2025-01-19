import json

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


@pytest.mark.django_db
def test_index_page_has_update_links_for_authorized_user(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
) -> None:
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    tds_name = parser.css("td[data-header='name'] a")
    edit_context_menu_btns = parser.css(
        "li a[aria-label='edit object']",
    )
    context_menu_btns = parser.css("table li[role='menuitem']")

    assert response.status_code == 200
    assert len(tds_name) == 10
    assert len(edit_context_menu_btns) == 10
    assert len(context_menu_btns) == 20

    for pk, td in enumerate(tds_name, 1):
        update_url = model.objects.get(pk=pk).get_update_url()
        assert update_url == td.attributes["hx-get"]

    for pk, btn in enumerate(edit_context_menu_btns, 1):
        update_url = model.objects.get(pk=pk).get_update_url()
        assert update_url == btn.attributes["href"]


@pytest.mark.django_db
def test_index_page_has_no_update_links_for_unauthorized_user(
    client: Client,
    urls: dict[str, str],
    model: type[Model],
) -> None:
    client.login(
        username="user_with_view_delete_perm",
        password="user_with_view_delete_perm",
    )
    response = client.get(urls["index"])

    parser = HTMLParser(response.content)

    tds_name = parser.css("td[data-header='name']")
    tds_name_href = parser.css("td[data-header='name'] a")
    edit_context_menu_btns = parser.css(
        "li a[aria-label='edit object']",
    )
    delete_context_menu_btns = parser.css(
        "table li[role='menuitem']",
    )
    update_response = client.get(
        model.objects.first().get_update_url(),
    )

    assert response.status_code == 200
    assert len(tds_name_href) == 0
    assert len(edit_context_menu_btns) == 0

    for pk, td in enumerate(tds_name, 1):
        update_url = model.objects.get(pk=pk).name
        assert update_url == td.text(strip=True)

    assert len(delete_context_menu_btns) == 10
    assert update_response.status_code == 403


@pytest.mark.django_db
def test_update_page(
    admin_client: Client,
    model: type[Model],
    templates: dict[str, str],
    app_label: str,
):
    obj = model.objects.first()
    response = admin_client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    h1 = parser.css_first("form h1").text(strip=True)
    form = parser.css_first("main form")
    name_input = form.css_first("input[name='name']")
    description_input = form.css_first(
        "textarea[name='description']",
    )
    required_star = form.css_first(
        "span[aria-label='required field']",
    )

    assert response.status_code == 200
    assert is_template_used(templates["update"], response)
    assert h1 == f"update {obj.name}"
    assert form.attributes["hx-post"] == obj.get_update_url()
    assert form.attributes["id"] == f"{app_label}-form"
    assert name_input.attributes["value"] == obj.name
    assert description_input.text(strip=True) == obj.description
    assert required_star is not None


@pytest.mark.django_db
def test_update_form_has_previous_page_querystring(
    admin_client: Client, model: type[Model]
):
    obj = model.objects.first()

    url = obj.get_update_url() + "?page=1&per_page=10&order_by=-Id"

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    form = parser.css_first("main form")

    assert response.status_code == 200
    assert form.attributes["hx-post"] == url


@pytest.mark.django_db
def test_update_with_dirty_data(
    admin_client: Client,
    model: type[Model],
    dirty_data: list[dict],
    templates: dict[str, str],
):
    obj = model.objects.first()
    url = obj.get_update_url()

    for data in dirty_data:
        response = admin_client.post(url, data["data"])
        assert data["error"] in response.content.decode()
        assert is_template_used(templates["update_form"], response)
        assert response.status_code == 200

    assert model.objects.count() == 304


@pytest.mark.django_db
def test_update_with_modal_with_dirty_data(
    admin_client: Client,
    model: type[Model],
    dirty_data: list[dict],
    urls: dict[str, str],
    templates: dict[str, str],
):
    obj = model.objects.first()
    url = obj.get_update_url() + "?page=1&per_page=10&order_by=-Id"

    headers = {
        "modal": True,
        "redirect-to": urls["index"],
        "querystring": "page=1&per_page=10&order_by=-Id",
    }

    for data in dirty_data:
        response = admin_client.post(
            url,
            data["data"],
            headers=headers,
        )
        assert data["error"] in response.content.decode()
        assert is_template_used(templates["update_modal_form"], response)
        assert response.status_code == 200

    assert model.objects.count() == 304


@pytest.mark.django_db
def test_update_form_with_clean_data(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    clean_data_sample: dict[str, str],
):
    querystring = "?page=1&per_page=10&order_by=-Id"
    obj = model.objects.get(id=1)
    url = obj.get_update_url() + querystring

    response = admin_client.post(url, clean_data_sample)
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]
    obj = model.objects.get(id=1)

    assert response.status_code == 200
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert response.headers.get("Hx-redirect") == urls["index"] + querystring
    assert response.headers.get("Hx-redirect") == urls["index"] + querystring
    assert model.objects.count() == 304
    assert obj.name == name
    assert obj.description == description


@pytest.mark.django_db
def test_update_with_redirect_from_modal(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
) -> None:
    obj = model.objects.get(id=1)
    url = obj.get_update_url() + "?per_page=10&order_by=-Id"

    headers = {
        "Hx-Request": "true",
        "modal": True,
        "redirect-to": urls["index"],
        "querystring": "per_page=10&order_by=-Id",
    }

    response = admin_client.get(url, headers=headers)
    parser = HTMLParser(response.content)
    form = parser.css_first("form")
    form_hx_post = form.attributes.get("hx-post")

    assert response.status_code == 200
    assert is_template_used(templates["update_modal_form"], response)
    assert form_hx_post == url

    response = admin_client.post(
        url,
        clean_data_sample,
        headers=headers,
    )

    location = json.loads(
        response.headers.get("Hx-Location", ""),
    )
    location_path = location.get("path")
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]

    assert location_path == urls["index"] + "per_page=10&order_by=-Id"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == 304

    obj = model.objects.get(id=1)

    assert obj.name == name
    assert obj.description == description


@pytest.mark.django_db
def test_update_without_redirect_from_modal(
    admin_client: Client,
    model: type[Model],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    obj = model.objects.get(id=4)
    url = obj.get_update_url() + "?per_page=10&order_by=-Id"

    response = admin_client.get(url, headers=headers_modal_GET)
    parser = HTMLParser(response.content)

    form = parser.css_first("form")
    form_hx_post = form.attributes.get("hx-post")

    assert response.status_code == 200
    assert is_template_used(templates["update_modal_form"], response)
    assert form_hx_post == url

    response = admin_client.post(
        url,
        clean_data_sample,
        headers=headers_modal_GET,
    )
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]

    assert response.headers.get("Hx-Location") is None
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == 304

    obj = model.objects.get(id=4)

    assert obj.name == name
    assert obj.description == description
