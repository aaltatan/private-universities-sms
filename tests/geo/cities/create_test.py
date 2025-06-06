import json

import pytest
from django.contrib import messages
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
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
):
    response = admin_client.get(urls["create"])
    parser = HTMLParser(response.content)

    h1 = parser.css_first("form h1").text(strip=True).lower()
    form = parser.css_first("main form")
    name_input = form.css_first("input[name='name']")
    kind_select = form.css_first("select[name='kind']")
    governorate_input = form.css_first("input[name='governorate']")
    create_governorate_btn = get_nested_create_btn(form, input_name="governorate")
    description_input = form.css_first("textarea[name='description']")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create"], response)

    assert h1 == "add new city"
    assert form.attributes["hx-post"] == urls["create"]
    assert form.attributes["id"] == f"{subapp_label}-form"

    assert name_input is not None
    assert kind_select is not None
    assert governorate_input is not None
    assert description_input is not None

    assert create_governorate_btn is not None
    assert get_nested_hx_path(create_governorate_btn) == reverse("geo:governorates:create")
    assert is_required_star_visible(form, "name")
    assert is_required_star_visible(form, "kind", input_type="select")
    assert is_required_star_visible(form, "governorate")


@pytest.mark.django_db
def test_add_nested_object_appearance_if_user_has_no_add_governorates_perm(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
):
    client.login(
        username=f"{subapp_label}_user_with_view_add_perm",
        password="password",
    )
    response = client.get(urls["create"])
    parser = HTMLParser(response.content)

    form = parser.css_first("main form")

    governorate_input = form.css_first("input[name='governorate']")
    create_governorate_btn = get_nested_create_btn(form, input_name="governorate")

    assert is_template_used(templates["create"], response)
    assert response.status_code == status.HTTP_200_OK
    assert governorate_input is not None
    assert is_required_star_visible(form, "governorate")
    assert create_governorate_btn is None


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
            data={"name": f"City {idx}", "governorate": 1},
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == f"City {idx}"

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
    assert last_obj.governorate.name == data["governorate"]
    assert last_obj.description == data["description"]
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
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert response.status_code == status.HTTP_201_CREATED
    assert model.objects.count() == objects_count + 1
    assert location.get("target") == target
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-name"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message

    data = clean_data_sample.copy()
    data["name"] = "afasfasf"
    data["save"] = "true"

    response = admin_client.post(url, data, headers=headers)
    location: dict = json.loads(
        response.headers.get("Hx-Location", {}),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert model.objects.count() == objects_count + 2
    assert location.get("target") == target
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-name"
