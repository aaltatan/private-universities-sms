import json

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
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

    assert response.status_code == status.HTTP_200_OK
    assert len(tds_name) == 10
    assert len(edit_context_menu_btns) == 10
    assert len(context_menu_btns) == 30

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
    app_label: str,
) -> None:
    client.login(
        username=f"{app_label}_user_with_view_delete_perm",
        password="password",
    )
    response = client.get(urls["index"])

    parser = HTMLParser(response.content)

    tds_name = parser.css("td[data-header='name']")
    tds_name_href = parser.css("td[data-header='name'] a")
    edit_context_menu_btns = parser.css("li a[aria-label='edit object']")
    delete_context_menu_btns = parser.css("table li[role='menuitem']")
    update_response = client.get(model.objects.first().get_update_url())

    assert response.status_code == status.HTTP_200_OK
    assert len(tds_name_href) == 0
    assert len(edit_context_menu_btns) == 0

    for pk, td in enumerate(tds_name, 1):
        update_url = model.objects.get(pk=pk).name
        assert update_url == td.text(strip=True)

    assert len(delete_context_menu_btns) == 10
    assert update_response.status_code == status.HTTP_403_FORBIDDEN


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
    description_input = form.css_first("textarea[name='description']")
    required_star = form.css_first("span[aria-label='required field']")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update"], response)
    assert h1 == f"update {obj.name}"
    assert form.attributes["hx-post"] == obj.get_update_url()
    assert form.attributes["id"] == f"{app_label}-form"
    assert name_input.attributes["value"] == obj.name
    assert description_input.text(strip=True) == obj.description
    assert required_star is not None


@pytest.mark.django_db
def test_update_with_dirty_data(
    admin_client: Client,
    model: type[Model],
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
    templates: dict[str, str],
    counts: dict[str, int],
):
    data, error, _ = dirty_data_test_cases
    obj = model.objects.first()
    url = obj.get_update_url()

    response = admin_client.post(url, data)
    assert error in response.content.decode()
    assert is_template_used(templates["update_form"], response)
    assert response.status_code == status.HTTP_200_OK

    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_update_with_modal_with_dirty_data(
    admin_client: Client,
    model: type[Model],
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
    templates: dict[str, str],
    headers_modal_GET: dict[str, str],
    app_label: str,
    counts: dict[str, int],
):
    data, error, _ = dirty_data_test_cases
    obj = model.objects.first()
    url = obj.get_update_url() + "?page=1&per_page=10&ordering=-Id"

    headers = {
        **headers_modal_GET,
        "target": f"#{app_label}-table",
    }

    response = admin_client.post(url, data, headers=headers)
    assert error in response.content.decode()
    assert is_template_used(templates["update_modal_form"], response)
    assert response.status_code == status.HTTP_200_OK

    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_update_form_with_clean_data(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    clean_data_sample: dict[str, str],
    counts: dict[str, int],
):
    querystring = "?page=1&per_page=10&ordering=-Id"
    obj = model.objects.get(id=1)
    url = obj.get_update_url() + querystring

    response = admin_client.post(url, clean_data_sample)
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]
    obj = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert response.headers.get("Hx-redirect") == urls["index"] + querystring
    assert model.objects.count() == counts["objects"]
    assert obj.name == name
    assert obj.description == description


@pytest.mark.django_db
def test_update_with_redirect_from_modal(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    headers_modal_GET: dict[str, str],
    app_label: str,
    counts: dict[str, int],
) -> None:
    obj = model.objects.get(id=1)
    url = obj.get_update_url() + "?per_page=10&ordering=-Id"

    headers = {
        **headers_modal_GET,
        "target": "#modal-container",
    }

    response = admin_client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update_modal_form"], response)

    headers["target"] = f"#{app_label}-table"
    response = admin_client.post(url, clean_data_sample, headers=headers)

    location: dict = json.loads(
        response.headers.get("Hx-Location", ""),
    )
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]

    assert location.get("target") == f"#{app_label}-table"
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-Id"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == counts["objects"]

    obj = model.objects.get(id=1)

    assert obj.name == name
    assert obj.description == description


@pytest.mark.django_db
def test_update_without_using_target_in_hx_request(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
) -> None:
    with pytest.raises(ValueError):
        admin_client.get(
            model.objects.first().get_update_url(),
            headers=headers_modal_GET,
        )


@pytest.mark.django_db
def test_update_without_redirect_from_modal(
    admin_client: Client,
    model: type[Model],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    headers_modal_GET: dict[str, str],
    counts: dict[str, int],
) -> None:
    obj = model.objects.get(id=4)
    url = obj.get_update_url() + "?per_page=10&ordering=-Id"

    headers = {
        **headers_modal_GET,
        "target": "#modal-container",
        "dont-redirect": "true",
    }

    response = admin_client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update_modal_form"], response)
    assert "Hx-Location" not in response.headers
    assert "Hx-Retarget" not in response.headers

    headers = {**headers, "target": "#no-content"}
    response = admin_client.post(url, clean_data_sample, headers=headers)
    messages_list = list(get_messages(request=response.wsgi_request))
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]

    assert response.headers.get("Hx-Location") is None
    assert response.headers.get("Hx-Redirect") is None
    assert response.headers.get("Hx-Retarget") is None
    assert response.headers.get("Hx-Reswap") == "innerHTML"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == counts["objects"]

    obj = model.objects.get(id=4)

    assert obj.name == name
    assert obj.description == description


@pytest.mark.django_db
def test_update_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    response: Response = api_client.put(
        path=f"{urls['api']}1/",
        data={
            "name": "Hamah",
            "description": "some description",
        },
        headers=admin_headers,
        follow=True,
    )
    first = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Hamah"
    assert response.json()["description"] == "some description"
    assert first.name == "Hamah"
    assert first.description == "some description"


@pytest.mark.django_db
def test_update_object_with_dirty_data(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
):
    data, _, error = dirty_data_test_cases
    response: Response = api_client.put(
        path=f"{urls['api']}3/", data=data, headers=admin_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["name"] == error
