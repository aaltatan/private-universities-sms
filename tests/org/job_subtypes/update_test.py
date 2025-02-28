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
from tests.utils import is_required_star_visible, is_template_used


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

    h1 = parser.css_first("form h1").text(strip=True).lower()
    form = parser.css_first("main form")
    name_input = form.css_first("input[name='name']")
    job_type_input = form.css_first("input[name='job_type']")
    create_job_type_btn = form.css_first(
        "div[role='group']:has(input[name='job_type']) div[aria-label='create nested object']"
    )
    description_input = form.css_first("textarea[name='description']")
    required_star = form.css_first("span[aria-label='required field']")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update"], response)
    assert h1 == f"update {obj.name}".lower()
    assert form.attributes["hx-post"] == obj.get_update_url()
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert "required" in name_input.attributes
    assert name_input.attributes["value"] == obj.name
    assert job_type_input.attributes["value"] == str(obj.job_type.pk)
    assert description_input.text(strip=True) == obj.description

    assert required_star is not None
    assert create_job_type_btn is not None
    assert is_required_star_visible(form, "name")
    assert is_required_star_visible(form, "job_type")


@pytest.mark.django_db
def test_add_nested_object_appearance_if_user_has_no_add_job_types_perm(
    client: Client,
    model: type[Model],
    templates: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_change_perm",
        password="password",
    )
    update_url = model.objects.first().get_update_url()
    response = client.get(update_url)
    parser = HTMLParser(response.content)

    form = parser.css_first("main form")

    job_type_input = form.css_first("input[name='job_type']")
    create_job_type_btn = form.css_first(
        "div[role='group']:has(input[name='job_type']) div[aria-label='create nested object']"
    )

    assert is_template_used(templates["update"], response)
    assert response.status_code == status.HTTP_200_OK
    assert job_type_input is not None
    assert is_required_star_visible(form, "job_type")
    assert create_job_type_btn is None


@pytest.mark.django_db
def test_update_form_with_clean_data(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    clean_data_sample: dict[str, str],
    counts: dict[str, int],
):
    querystring = "?page=1&per_page=10&ordering=-id"
    obj = model.objects.get(id=1)
    url = obj.get_update_url() + querystring

    clean_data_sample["update"] = "true"
    response = admin_client.post(url, clean_data_sample)
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    job_type = clean_data_sample["job_type"]
    description = clean_data_sample["description"]
    obj = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert response.headers.get("Hx-redirect") == urls["index"] + querystring
    assert model.objects.count() == counts["objects"]
    assert obj.name == name
    assert obj.job_type.name == job_type
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
    url = obj.get_update_url() + "?per_page=10&ordering=-id"

    headers = {
        **headers_modal_GET,
        "target": "#modal-container",
    }

    response = admin_client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update_modal_form"], response)

    headers["target"] = f"#{subapp_label}-table"
    clean_data_sample["update"] = "true"
    response = admin_client.post(url, clean_data_sample, headers=headers)

    location: dict = json.loads(
        response.headers.get("Hx-Location", ""),
    )
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    name = clean_data_sample["name"]
    job_type = clean_data_sample["job_type"]
    description = clean_data_sample["description"]

    assert location.get("target") == f"#{subapp_label}-table"
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-id"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == counts["objects"]

    obj = model.objects.get(id=1)

    assert obj.name == name
    assert obj.job_type.name == job_type
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
    url = obj.get_update_url() + "?per_page=10&ordering=-id"

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
    clean_data_sample["update"] = "true"
    response = admin_client.post(url, clean_data_sample, headers=headers)
    messages_list = list(get_messages(request=response.wsgi_request))

    name = clean_data_sample["name"]
    job_type = clean_data_sample["job_type"]
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
    assert obj.job_type.name == job_type
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
            "job_type": 3,
            "description": "some description",
        },
        headers=admin_headers,
        follow=True,
    )
    first = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == first.name == "Hamah"
    assert response.json()["description"] == first.description == "some description"
    assert response.json()["job_type"] == first.job_type.id == 3


@pytest.mark.django_db
def test_patch_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    response: Response = api_client.patch(
        path=f"{urls['api']}1/",
        data={"job_type": 3},
        headers=admin_headers,
        follow=True,
    )
    first = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == first.name
    assert response.json()["description"] == first.description
    assert response.json()["job_type"] == first.job_type.id == 3
