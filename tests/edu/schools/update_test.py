import json

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import (
    get_nested_create_btn,
    get_nested_hx_path,
    is_required_star_visible,
    is_template_used,
)


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
    nationality_input = form.css_first("input[name='nationality']")
    kind_input = form.css_first("input[name='kind']")
    website_input = form.css_first("input[name='website']")
    email_input = form.css_first("input[name='email']")
    phone_input = form.css_first("input[name='phone']")
    description_input = form.css_first("textarea[name='description']")
    required_star = form.css_first("span[aria-label='required field']")
    nationality_create_btn = get_nested_create_btn(form, input_name="nationality")
    kind_create_btn = get_nested_create_btn(form, input_name="kind")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update"], response)
    assert h1 == f"update {obj.name}".lower()
    assert form.attributes["hx-post"] == obj.get_update_url()
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert "required" in name_input.attributes
    assert name_input.attributes["value"] == obj.name
    assert description_input.text(strip=True) == obj.description
    assert nationality_input.attributes["value"] == str(obj.nationality.pk)
    assert kind_input.attributes["value"] == str(obj.kind.pk)
    assert website_input.attributes["value"] == obj.website
    assert email_input.attributes["value"] == obj.email
    assert phone_input.attributes["value"] == obj.phone

    assert required_star is not None
    assert is_required_star_visible(form, "name")
    assert is_required_star_visible(form, "nationality")
    assert is_required_star_visible(form, "kind")
    assert not is_required_star_visible(form, "website")
    assert not is_required_star_visible(form, "email")
    assert not is_required_star_visible(form, "phone")

    assert nationality_create_btn is not None
    assert kind_create_btn is not None
    assert get_nested_hx_path(nationality_create_btn) == reverse("geo:nationalities:create")
    assert get_nested_hx_path(kind_create_btn) == reverse("edu:school_kinds:create")


@pytest.mark.django_db
def test_update_page_without_perms_for_creating_nested_objects(
    client: Client,
    model: type[Model],
    templates: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_change_perm",
        password="password",
    )
    obj = model.objects.first()
    response = client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    h1 = parser.css_first("form h1").text(strip=True).lower()
    form = parser.css_first("main form")
    name_input = form.css_first("input[name='name']")
    nationality_input = form.css_first("input[name='nationality']")
    kind_input = form.css_first("input[name='kind']")
    website_input = form.css_first("input[name='website']")
    email_input = form.css_first("input[name='email']")
    phone_input = form.css_first("input[name='phone']")
    description_input = form.css_first("textarea[name='description']")
    required_star = form.css_first("span[aria-label='required field']")
    nationality_create_btn = get_nested_create_btn(form, input_name="nationality")
    kind_create_btn = get_nested_create_btn(form, input_name="kind")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["update"], response)
    assert h1 == f"update {obj.name}".lower()
    assert form.attributes["hx-post"] == obj.get_update_url()
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert "required" in name_input.attributes
    assert name_input.attributes["value"] == obj.name
    assert description_input.text(strip=True) == obj.description
    assert nationality_input.attributes["value"] == str(obj.nationality.pk)
    assert kind_input.attributes["value"] == str(obj.kind.pk)
    assert website_input.attributes["value"] == obj.website
    assert email_input.attributes["value"] == obj.email
    assert phone_input.attributes["value"] == obj.phone

    assert required_star is not None
    assert is_required_star_visible(form, "name")
    assert is_required_star_visible(form, "nationality")
    assert is_required_star_visible(form, "kind")
    assert not is_required_star_visible(form, "website")
    assert not is_required_star_visible(form, "email")
    assert not is_required_star_visible(form, "phone")

    assert nationality_create_btn is None
    assert kind_create_btn is None


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
    nationality = clean_data_sample["nationality"]
    kind = clean_data_sample["kind"]
    website = clean_data_sample["website"]
    email = clean_data_sample["email"]
    phone = clean_data_sample["phone"]
    description = clean_data_sample["description"]
    obj = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert response.headers.get("Hx-redirect") == urls["index"] + querystring
    assert model.objects.count() == counts["objects"]
    assert obj.name == name
    assert obj.nationality.name == nationality
    assert obj.kind.name == kind
    assert obj.website == website
    assert obj.email == email
    assert obj.phone == phone
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
    nationality = clean_data_sample["nationality"]
    kind = clean_data_sample["kind"]
    website = clean_data_sample["website"]
    email = clean_data_sample["email"]
    phone = clean_data_sample["phone"]
    description = clean_data_sample["description"]

    assert location.get("target") == f"#{subapp_label}-table"
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-id"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"({name}) has been updated successfully"
    assert model.objects.count() == counts["objects"]

    obj = model.objects.get(id=1)

    assert obj.name == name
    assert obj.description == description
    assert obj.nationality.name == nationality
    assert obj.kind.name == kind
    assert obj.website == website
    assert obj.email == email
    assert obj.phone == phone


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
    description = clean_data_sample["description"]
    nationality = clean_data_sample["nationality"]
    kind = clean_data_sample["kind"]
    website = clean_data_sample["website"]
    email = clean_data_sample["email"]
    phone = clean_data_sample["phone"]

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
    assert obj.nationality.name == nationality
    assert obj.kind.name == kind
    assert obj.website == website
    assert obj.email == email
    assert obj.phone == phone


@pytest.mark.django_db
def test_update_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    nationality_model: type[Model],
    school_kind_model: type[Model],
):
    response: Response = api_client.put(
        path=f"{urls['api']}1/",
        data={
            "name": "Hamah",
            "nationality": 1,
            "kind": 1,
            "website": "https://www.google.com",
            "email": "a.altatan@gmail.com",
            "phone": "1234567890",
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
    assert first.nationality.name == "Nationality 001"
    assert first.kind.name == "SchoolKind 001"
    assert first.website == "https://www.google.com"
    assert first.email == "a.altatan@gmail.com"
    assert first.phone == "1234567890"
    assert first.description == "some description"


@pytest.mark.django_db
def test_patch_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    response: Response = api_client.patch(
        path=f"{urls['api']}1/",
        data={
            "description": "new description",
        },
        headers=admin_headers,
        follow=True,
    )
    first = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == first.name
    assert response.json()["description"] == "new description"
    assert response.json()["nationality"] == first.nationality.pk
    assert response.json()["kind"] == first.kind.pk
    assert response.json()["website"] == first.website
    assert response.json()["email"] == first.email
    assert response.json()["phone"] == first.phone
    assert first.description == "new description"
