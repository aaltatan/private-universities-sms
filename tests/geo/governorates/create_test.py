import json

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from django.utils.text import slugify
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model
from tests.common import create
from tests.utils import is_template_used


@pytest.mark.django_db
def test_add_new_btn_appearance_if_user_has_no_add_perm(
    client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    subapp_label: str,
) -> None:
    create.test_add_new_btn_appearance_if_user_has_no_add_perm(
        client, urls, templates, subapp_label
    )


@pytest.mark.django_db
def test_send_request_to_create_page_without_permission(
    client: Client, urls: dict[str, str], subapp_label: str
) -> None:
    create.test_send_request_to_create_page_without_permission(
        client, urls, subapp_label
    )


@pytest.mark.django_db
def test_add_new_btn_appearance_if_user_has_add_perm(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    create.test_add_new_btn_appearance_if_user_has_add_perm(
        admin_client, urls, templates
    )


@pytest.mark.django_db
def test_send_request_to_create_page_with_permission(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
) -> None:
    create.test_send_request_to_create_page_with_permission(
        admin_client, urls, templates
    )


@pytest.mark.django_db
def test_create_from_modal_without_using_target_in_hx_request(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    create.test_create_from_modal_without_using_target_in_hx_request(
        admin_client, urls, headers_modal_GET
    )


@pytest.mark.django_db
def test_create_object_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    create.test_create_object_without_permissions(api_client, urls, user_headers)


@pytest.mark.django_db
def test_create_new_object_with_save_btn(
    model: type[Model],
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    counts: dict[str, int],
) -> None:
    create.test_create_new_object_with_save_btn(
        model, admin_client, urls, templates, clean_data_sample, counts
    )


@pytest.mark.django_db
def test_create_from_modal_without_using_save_or_save_and_add_another(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    clean_data_sample: dict[str, str],
) -> None:
    create.test_create_from_modal_without_using_save_or_save_and_add_another(
        admin_client, urls, headers_modal_GET, clean_data_sample
    )


@pytest.mark.django_db
def test_create_without_redirect_from_modal(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    clean_data_sample: dict[str, str],
    model: type[Model],
    headers_modal_GET: dict[str, str],
    counts: dict[str, int],
) -> None:
    create.test_create_without_redirect_from_modal(
        admin_client,
        urls,
        templates,
        clean_data_sample,
        model,
        headers_modal_GET,
        counts,
    )


@pytest.mark.django_db
def test_create_new_object_with_dirty_or_duplicated_data(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: type[Model],
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
    counts: dict[str, int],
) -> None:
    create.test_create_new_object_with_dirty_or_duplicated_data(
        admin_client, urls, templates, model, dirty_data_test_cases, counts
    )


@pytest.mark.django_db
def test_create_object_with_dirty_data(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
):
    create.test_create_object_with_dirty_data(
        api_client, urls, admin_headers, dirty_data_test_cases
    )


@pytest.mark.django_db
def test_create_new_object_with_modal_with_dirty_or_duplicated_data(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    model: type[Model],
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
    headers_modal_GET: dict[str, str],
    subapp_label: str,
    counts: dict[str, int],
) -> None:
    create.test_create_new_object_with_modal_with_dirty_or_duplicated_data(
        admin_client,
        urls,
        templates,
        model,
        dirty_data_test_cases,
        headers_modal_GET,
        subapp_label,
        counts,
    )


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
            data={"name": f"City {idx}"},
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == f"City {idx}"

    response: Response = api_client.get(
        path=urls["api"],
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == objects_count + batch_size
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
    url = urls["create"] + "?per_page=10&ordering=-Name"
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
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-Name"
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
    assert location.get("path") == urls["index"] + "?per_page=10&ordering=-Name"
