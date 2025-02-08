import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from django.utils.text import slugify
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


def test_create_from_modal_without_using_target_in_hx_request(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    with pytest.raises(ValueError, match="target is required"):
        admin_client.get(urls["create"], headers=headers_modal_GET)


def test_create_object_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    response = api_client.post(
        path=urls["api"], data={"name": "City"}, headers=user_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response: Response = api_client.post(
        path=urls["api"],
        data={"name": "City"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_new_btn_appearance_if_user_has_no_add_perm(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
) -> None:
    client.login(
        username=f"{subapp_label}_user_with_view_perm_only",
        password="password",
    )

    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("[aria-label='create new object']")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)
    assert btn is None


def test_send_request_to_create_page_without_permission(
    client: Client, urls: dict[str, str], subapp_label: str
) -> None:
    client.login(
        username=f"{subapp_label}_user_with_view_perm_only",
        password="password",
    )
    response = client.get(urls["create"])
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_add_new_btn_appearance_if_user_has_add_perm(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("[aria-label='create new object']")

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)
    assert btn is not None


def test_send_request_to_create_page_with_permission(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    response = admin_client.get(urls["create"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create"], response)


def test_create_new_object_with_save_btn(
    model: type[Model],
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    counts: dict[str, int],
) -> None:
    objects_count = counts["objects"]
    response = admin_client.get(urls["create"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create"], response)

    clean_data_sample["save"] = "true"
    response = admin_client.post(urls["create"], clean_data_sample)
    messages_list = list(
        get_messages(request=response.wsgi_request),
    )
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert is_template_used(templates["create_form"], response, False)
    assert is_template_used(templates["create_modal_form"], response, False)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get("Hx-Redirect") is not None
    assert response.headers.get("Hx-Trigger") == "messages"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message
    assert model.objects.count() == objects_count + 1


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
    qs = model.objects.all()
    last_obj = qs.last()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get("Hx-Trigger") == "messages"
    assert is_template_used(templates["create_form"], response)
    assert last_obj.pk == objects_count + 1
    assert last_obj.name == data["name"]
    assert last_obj.description == data["description"]
    assert last_obj.slug == slugify(data["name"], allow_unicode=True)
    assert qs.count() == objects_count + 1


def test_create_from_modal_without_using_save_or_save_and_add_another(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    clean_data_sample: dict[str, str],
) -> None:
    headers = {**headers_modal_GET, "target": "#modal-container"}
    with pytest.raises(
        ValueError,
        match="save or save_and_add_another is required",
    ):
        admin_client.post(urls["create"], clean_data_sample, headers=headers)


def test_create_without_redirect_from_modal(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
    headers_modal_GET: dict[str, str],
    counts: dict[str, int],
) -> None:
    objects_count = counts["objects"]
    headers = {
        **headers_modal_GET,
        "target": "#modal-container",
    }
    response = admin_client.get(urls["create"], headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["create_modal_form"], response)

    headers = {
        **headers,
        "dont-redirect": "true",
        "target": "#no-content",
    }
    sample = {**clean_data_sample, "save": "true"}
    response = admin_client.post(urls["create"], sample, headers=headers)
    messages_list = list(get_messages(request=response.wsgi_request))
    success_message = f"{clean_data_sample['name']} has been created successfully"

    assert response.status_code == status.HTTP_201_CREATED
    assert is_template_used(templates["create_modal_form"], response, used=False)
    assert is_template_used(templates["create_form"], response, used=False)
    assert is_template_used(templates["create"], response, used=False)
    assert model.objects.count() == objects_count + 1
    assert response.headers.get("Hx-Redirect") is None
    assert response.headers.get("Hx-Location") is None
    assert response.headers.get("Hx-Reswap") == "innerHTML"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == success_message
