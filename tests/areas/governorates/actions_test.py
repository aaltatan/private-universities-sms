import json
import re

import pytest
import pytest_mock
from django.contrib import messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_bulk_delete_modal_response(
    admin_client: Client,
    urls: dict[str, str],
    counts: dict[str, int],
):
    bulk_delete_batch = counts["bulk_delete_batch"]
    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "modal",
        "name": "delete",
    }
    response = admin_client.post(urls["index"], data)
    parser = HTMLParser(response.content)
    modal_body = (
        parser.css_first(
            "#modal-container > div > form > div:nth-child(2) p",
        )
        .text(strip=True)
        .replace("\n", "")
        .strip()
    )
    modal_body = re.compile(r"\s{2,}").sub(" ", modal_body)

    assert response.status_code == status.HTTP_200_OK
    assert (
        modal_body
        == f"are you sure you want to delete all {bulk_delete_batch} selected objects ?"
    )


@pytest.mark.django_db
def test_bulk_delete_without_permissions(
    client: Client,
    urls: dict[str, str],
    app_label: str,
    counts: dict[str, int],
):
    bulk_delete_batch = counts["bulk_delete_batch"]
    client.login(
        username=f"{app_label}_user_with_view_perm_only",
        password="password",
    )

    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "delete",
    }

    response = client.post(urls["index"], data, follow=True)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_bulk_delete_with_permissions(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    bulk_delete_batch = counts["bulk_delete_batch"]
    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "delete",
    }

    response = admin_client.post(urls["index"], data)
    hx_location = json.loads(
        response.headers.get("Hx-Location"),
    )
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.headers.get("Hx-Location") is not None
    assert hx_location["path"] == urls["index"]
    assert messages_list[0].level == messages.SUCCESS
    assert (
        messages_list[0].message
        == "all selected 50 objects have been deleted successfully."
    )
    assert model.objects.count() == objects_count - bulk_delete_batch


@pytest.mark.django_db
def test_bulk_delete_with_permissions_with_undeletable_objects(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    bulk_delete_batch = counts["bulk_delete_batch"]
    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "delete",
    }
  
    mocker.patch(
        f"apps.areas.{app_label}.utils.Deleter.is_qs_deletable",
        return_value=False,
    )

    response = admin_client.post(urls["index"], data)
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("Hx-Location") is None
    assert response.headers.get("Hx-Retarget") == "#no-content"
    assert response.headers.get("HX-Reswap") == "innerHTML"
    assert response.headers.get("HX-Trigger") == "messages"
    assert messages_list[0].level == messages.ERROR
    assert messages_list[0].message == "selected 50 objects cannot be deleted."
    assert model.objects.count() == objects_count


@pytest.mark.django_db
def test_bulk_action_not_found(
    admin_client: Client,
    urls: dict[str, str],
    counts: dict[str, int],
):
    bulk_delete_batch = counts["bulk_delete_batch"]
    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "bulk_delete",  # name not in actions
    }

    response = admin_client.post(urls["index"], data)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    response = admin_client.post(urls["index"], data, follow=True)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_bulk_delete_with_permissions_only_for_view(
    client: Client,
    urls: dict[str, str],
    app_label: str,
    counts: dict[str, int],
):
    bulk_delete_batch = counts["bulk_delete_batch"]
    client.login(
        username=f"{app_label}_user_with_view_perm_only",
        password="password",
    )

    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "delete",
    }

    response = client.post(urls["index"], data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_bulk_delete_when_no_deleter_class_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    counts: dict[str, int],
):
    bulk_delete_batch = counts["bulk_delete_batch"]
    mocker.patch(f"apps.areas.{app_label}.views.ListView.deleter", new=None)
    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "delete",
    }
    with pytest.raises(AttributeError):
        admin_client.post(urls["index"], data)


@pytest.mark.django_db
def test_bulk_delete_when_deleter_class_is_not_subclass_of_Deleter(
    admin_client: Client,
    urls: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    counts: dict[str, int],
):
    bulk_delete_batch = counts["bulk_delete_batch"]

    class Deleter:
        pass

    mocker.patch(f"apps.areas.{app_label}.views.ListView.deleter", new=Deleter)
    data: dict = {
        "action-check": list(range(1, bulk_delete_batch + 1)),
        "kind": "action",
        "name": "delete",
    }
    with pytest.raises(TypeError):
        admin_client.post(urls["index"], data)


@pytest.mark.django_db
def test_bulk_delete_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [1, 2, 3, 4, 500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert model.objects.count() == objects_count - 4

    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert model.objects.count() == objects_count - 4


@pytest.mark.django_db
def test_bulk_delete_objects_undeletable(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    mocker.patch(
        f"apps.areas.{app_label}.utils.Deleter.is_qs_deletable",
        return_value=False,
    )

    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [1, 2, 3, 4, 500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["details"] == "selected 4 objects cannot be deleted."
    assert model.objects.count() == objects_count

    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert model.objects.count() == objects_count
