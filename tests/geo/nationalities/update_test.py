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
def test_update_page(
    admin_client: Client,
    model: type[Model],
    templates: dict[str, str],
    subapp_label: str,
):
    obj = model.objects.first()
    response = admin_client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    h1 = parser.css_first("form h1").text(strip=True)
    form = parser.css_first("main form")
    name_input = form.css_first("input[name='name']")
    name_input_required_star = form.css_first(
        "div[role='group']:has(input[name='name']) span[aria-label='required field']"
    )
    is_local_select_options = form.css("select[name='is_local'] option")
    description_input = form.css_first("textarea[name='description']")
    required_star = form.css_first("span[aria-label='required field']")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update"], response)
    assert h1 == f"update {obj.name}"
    assert form.attributes["hx-post"] == obj.get_update_url()
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert "required" in name_input.attributes
    assert name_input.attributes["value"] == obj.name
    for option in is_local_select_options:
        if option.attributes.get("selected"):
            assert option.text(strip=True) == "Foreign"
    assert description_input.text(strip=True) == obj.description

    assert required_star is not None
    assert name_input_required_star is not None


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
    assert obj.is_local
    assert obj.description == description


@pytest.mark.django_db
def test_update_with_redirect_from_modal(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    headers_modal_GET: dict[str, str],
    subapp_label: str,
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

    headers["target"] = f"#{subapp_label}-table"
    response = admin_client.post(url, clean_data_sample, headers=headers)

    location: dict = json.loads(
        response.headers.get("Hx-Location", ""),
    )
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    description = clean_data_sample["description"]

    assert location.get("target") == f"#{subapp_label}-table"
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-Id"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == counts["objects"]

    obj = model.objects.get(id=1)

    assert obj.name == name
    assert obj.is_local
    assert obj.description == description


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
    assert obj.is_local
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
    assert response.json()["is_local"] is False
    assert response.json()["description"] == "some description"
    assert first.name == "Hamah"
    assert first.description == "some description"
