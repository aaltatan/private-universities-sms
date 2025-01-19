import json

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from django.utils.text import slugify
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


@pytest.mark.django_db
def test_add_new_btn_appearance_if_user_has_no_add_perm(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )

    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("[aria-label='create new object']")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert btn is None


@pytest.mark.django_db
def test_send_request_to_create_page_without_permission(
    client: Client, urls: dict[str, str]
) -> None:
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )
    response = client.get(urls["create"])
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_new_btn_appearance_if_user_has_add_perm(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("[aria-label='create new object']")

    assert response.status_code == 200
    assert is_template_used(templates["index"], response)
    assert btn is not None


@pytest.mark.django_db
def test_send_request_to_create_page_with_permission(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    response = admin_client.get(urls["create"])

    assert response.status_code == 200
    assert is_template_used(templates["create"], response)


@pytest.mark.django_db
def test_create_new_object_with_save_btn(
    model: type[Model],
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
) -> None:
    response = admin_client.get(urls["create"])

    assert response.status_code == 200
    assert is_template_used(templates["create"], response)

    clean_data_sample["save"] = "true"
    response = admin_client.post(urls["create"], clean_data_sample)
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert response.status_code == 201
    assert response.headers.get("Hx-Redirect") is not None
    assert response.headers.get("Hx-Trigger") == "messages"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message
    assert model.objects.count() == 305


@pytest.mark.django_db
def test_create_new_object_with_save_and_add_another_btn(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
) -> None:
    response = admin_client.get(urls["create"])

    assert response.status_code == 200
    assert is_template_used(templates["create"], response)

    data = clean_data_sample.copy()
    data["save_and_add_another"] = "true"

    response = admin_client.post(urls["create"], data)
    qs = model.objects.all()
    last_obj = qs.last()

    assert response.status_code == 201
    assert response.headers.get("Hx-Trigger") == "messages"
    assert is_template_used(templates["create_form"], response)
    assert last_obj.pk == 305
    assert last_obj.name == data["name"]
    assert last_obj.description == data["description"]
    assert last_obj.slug == slugify(data["name"], allow_unicode=True)
    assert qs.count() == 305


@pytest.mark.django_db
def test_create_simulating_create_without_redirect_from_modal(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
    headers_modal_GET: dict[str, str],
) -> None:
    response = admin_client.get(urls["create"], headers=headers_modal_GET)

    assert response.status_code == 200
    assert is_template_used(templates["create_modal_form"], response)

    response = admin_client.post(
        urls["create"],
        clean_data_sample,
        headers=headers_modal_GET,
    )
    messages_list = list(get_messages(request=response.wsgi_request))
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert response.status_code == 201
    assert is_template_used(templates["create_modal_form"], response, used=False)
    assert model.objects.count() == 305
    assert response.headers.get("Hx-Redirect") is None
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message


@pytest.mark.django_db
def test_create_simulating_create_with_redirect_from_modal(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
    headers_modal_GET: dict[str, str],
) -> None:
    url = urls["create"] + "?per_page=10&order_by=-Name"
    response = admin_client.get(url, headers=headers_modal_GET)

    assert response.status_code == 200
    assert is_template_used(templates["create_modal_form"], response)

    headers = {
        "modal": True,
        "redirect-to": urls["index"],
        "querystring": "per_page=10&order_by=-Name",
    }
    data = clean_data_sample.copy()
    data["save"] = "true"

    response = admin_client.post(url, data, headers=headers)
    location: dict = json.loads(response.headers.get("Hx-Location", {}))
    location_path = location.get("path")
    messages_list = list(get_messages(request=response.wsgi_request))
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert response.status_code == 201
    assert model.objects.count() == 305
    assert location_path == urls["index"] + "per_page=10&order_by=-Name"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message

    headers = {"modal": True, "redirect-to": urls["index"]}

    data = clean_data_sample.copy()
    data["name"] = "afasfasf"
    data["save"] = "true"

    response = admin_client.post(url, data, headers=headers)
    location: dict = json.loads(
        response.headers.get("Hx-Location", {}),
    )
    location_path = location.get("path")

    assert response.status_code == 201
    assert model.objects.count() == 306
    assert location_path == urls["index"]


@pytest.mark.django_db
def test_create_new_object_with_dirty_or_duplicated_data(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: type[Model],
    dirty_data: list[dict],
) -> None:
    response = admin_client.get(urls["create"])

    assert response.status_code == 200
    assert is_template_used(templates["create"], response)

    for item in dirty_data:
        response = admin_client.post(urls["create"], item["data"])
        parser = HTMLParser(response.content)
        form_hx_post = parser.css_first(
            "form[hx-post]",
        ).attributes.get("hx-post")

        assert item["error"] in response.content.decode()
        assert is_template_used(templates["create_form"], response)
        assert response.status_code == 200
        assert form_hx_post == urls["create"]
        assert model.objects.count() == 304


@pytest.mark.django_db
def test_create_new_object_with_modal_with_dirty_or_duplicated_data(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: type[Model],
    dirty_data: list[dict],
    headers_modal_GET: dict[str, str],
) -> None:
    url = urls["create"] + "?per_page=10&order_by=-Name"
    headers = headers_modal_GET
    response = admin_client.get(url, headers=headers)

    assert response.status_code == 200
    assert is_template_used(templates["create_modal_form"], response)

    for item in dirty_data:
        response = admin_client.post(
            urls["create"],
            item["data"],
            headers=headers_modal_GET,
        )
        parser = HTMLParser(response.content)
        form_hx_post = parser.css_first(
            "form[hx-post]",
        ).attributes.get("hx-post")

        assert item["error"] in response.content.decode()
        assert is_template_used(templates["create_modal_form"], response)
        assert response.status_code == 200
        assert form_hx_post == urls["create"]
        assert model.objects.count() == 304
