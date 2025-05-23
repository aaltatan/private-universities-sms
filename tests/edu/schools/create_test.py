import json

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from django.urls import reverse
from django.utils.text import slugify
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
def test_create_page(
    admin_client: Client,
    templates: dict[str, str],
    urls: dict[str, str],
    subapp_label: str,
):
    response = admin_client.get(urls["create"])
    parser = HTMLParser(response.content)

    h1 = parser.css_first("form h1").text(strip=True).lower()
    form = parser.css_first("main form")
    description_input = form.css_first("textarea[name='description']")
    name_input = form.css_first("input[name='name']")
    nationality_input = form.css_first("input[name='nationality']")
    kind_input = form.css_first("input[name='kind']")
    website_input = form.css_first("input[name='website']")
    email_input = form.css_first("input[name='email']")
    phone_input = form.css_first("input[name='phone']")

    nationality_create_btn = get_nested_create_btn(form=form, input_name="nationality")
    kind_create_btn = get_nested_create_btn(form=form, input_name="kind")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create"], response)

    assert h1 == "add new school"
    assert form.attributes["hx-post"] == urls["create"]
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert name_input is not None
    assert nationality_input is not None
    assert kind_input is not None
    assert website_input is not None
    assert email_input is not None
    assert phone_input is not None
    assert description_input is not None

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
def test_create_page_without_perms_for_creating_nested_objects(
    client: Client,
    templates: dict[str, str],
    urls: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_add_perm",
        password="password",
    )
    response = client.get(urls["create"])
    parser = HTMLParser(response.content)

    h1 = parser.css_first("form h1").text(strip=True).lower()
    form = parser.css_first("main form")
    description_input = form.css_first("textarea[name='description']")
    name_input = form.css_first("input[name='name']")
    nationality_input = form.css_first("input[name='nationality']")
    kind_input = form.css_first("input[name='kind']")
    website_input = form.css_first("input[name='website']")
    email_input = form.css_first("input[name='email']")
    phone_input = form.css_first("input[name='phone']")

    nationality_create_btn = get_nested_create_btn(form=form, input_name="nationality")
    kind_create_btn = get_nested_create_btn(form=form, input_name="kind")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create"], response)

    assert h1 == "add new school"
    assert form.attributes["hx-post"] == urls["create"]
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert name_input is not None
    assert nationality_input is not None
    assert kind_input is not None
    assert website_input is not None
    assert email_input is not None
    assert phone_input is not None
    assert description_input is not None

    assert is_required_star_visible(form, "name")
    assert is_required_star_visible(form, "nationality")
    assert is_required_star_visible(form, "kind")
    assert not is_required_star_visible(form, "website")
    assert not is_required_star_visible(form, "email")
    assert not is_required_star_visible(form, "phone")

    assert nationality_create_btn is None
    assert kind_create_btn is None


@pytest.mark.django_db
def test_create_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    batch_size = counts["bulk_delete_batch"]
    for idx in range(10_000, 10_000 + batch_size):
        response = api_client.post(
            path=urls["api"],
            data={
                "name": f"School {idx}",
                "nationality": 1,
                "kind": 1,
                "website": f"https://www.google-{idx}.com",
                "email": f"a.altatan-{idx}@gmail.com",
                "phone": "1234567890",
                "description": f"School {idx}",
            },
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == f"School {idx}"

    response: Response = api_client.get(
        path=urls["api"],
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["meta"]["results_count"] == objects_count + batch_size
    assert model.objects.count() == objects_count + batch_size


@pytest.mark.django_db
def test_create_new_object_with_save_and_add_another_btn(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
) -> None:
    objects_count = counts["objects"]
    response = admin_client.get(urls["create"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create"], response)

    data = clean_data_sample.copy()
    data["save_and_add_another"] = "true"

    response = admin_client.post(urls["create"], data)
    qs = model.objects.all().order_by("-id")
    last_obj = qs.first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get("Hx-Trigger") == "messages"
    assert is_template_used(templates["create_form"], response)

    assert last_obj.pk == objects_count + 1
    assert last_obj.name == data["name"]
    assert last_obj.description == data["description"]
    assert last_obj.nationality.name == data["nationality"]
    assert last_obj.kind.name == data["kind"]
    assert last_obj.website == data["website"]
    assert last_obj.email == data["email"]
    assert last_obj.phone == data["phone"]
    assert last_obj.slug == slugify(data["name"], allow_unicode=True)

    assert qs.count() == objects_count + 1


@pytest.mark.django_db
def test_create_with_redirect_from_modal(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
    headers_modal_GET: dict[str, str],
    subapp_label: str,
    counts: dict[str, int],
) -> None:
    objects_count = counts["objects"]
    url = urls["create"] + "?per_page=10&ordering=-name"
    headers = {
        **headers_modal_GET,
        "target": "#modal-container",
    }
    response = admin_client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create_modal_form"], response)

    data = clean_data_sample.copy()
    data["save"] = "true"

    target = f"#{subapp_label}-table"
    headers = {**headers, "target": target}

    response = admin_client.post(url, data, headers=headers)
    location: dict = json.loads(response.headers.get("Hx-Location", {}))
    messages_list = list(get_messages(request=response.wsgi_request))
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert response.status_code == status.HTTP_201_CREATED
    assert model.objects.count() == objects_count + 1
    assert location.get("target") == target
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-name"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message

    data = clean_data_sample.copy()
    data["name"] = "afasfasfdas"
    data["email"] = "afasfasfdas@gmail.com"
    data["website"] = "https://afasfasfdas.com"
    data["save"] = "true"

    response = admin_client.post(url, data, headers=headers)
    location: dict = json.loads(
        response.headers.get("Hx-Location", ""),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert model.objects.count() == objects_count + 2
    assert location.get("target") == target
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-name"
