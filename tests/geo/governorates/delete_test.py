import pytest
import pytest_mock
from django.contrib import messages
from django.test import Client
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model
from apps.core.utils import Deleter
from apps.geo.models import Governorate


class CustomDeleter(Deleter[Governorate]):
    error_obj_msg = "error obj message"
    error_qs_msg = "error qs message"

    def check_obj_deleting_possibility(self, obj: Governorate) -> bool:
        return obj.pk not in [1, 2]

    def check_queryset_deleting_possibility(self, qs) -> bool:
        return not qs.filter(pk__in=[1, 2]).exists()


@pytest.mark.django_db
def test_delete_object_not_deletable(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    mocker.patch(
        f"apps.{app_label}.views.{subapp_label}.DeleteView.deleter", new=CustomDeleter
    )

    delete_url = model.objects.order_by("id").first().get_delete_url()
    response = admin_client.post(delete_url, headers=headers_modal_GET)
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )

    assert response.status_code == 200
    assert messages_list[0].level == messages.ERROR
    assert messages_list[0].message == "error obj message"
    assert model.objects.count() == 304


@pytest.mark.django_db
def test_api_delete_object_not_deletable(
    api_client: APIClient,
    admin_headers: dict[str, str],
    urls: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    mocker.patch(
        f"apps.{app_label}.views.{subapp_label}.APIViewSet.deleter", new=CustomDeleter
    )

    delete_url = f"{urls['api']}1/"

    response = api_client.delete(delete_url, headers=admin_headers)

    assert response.status_code == 400
    assert model.objects.count() == 304
    assert response.json()["details"] == "error obj message"


@pytest.mark.django_db
def test_api_delete_objects_not_deletable(
    api_client: APIClient,
    admin_headers: dict[str, str],
    urls: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    mocker.patch(
        f"apps.{app_label}.views.{subapp_label}.APIViewSet.deleter", new=CustomDeleter
    )

    delete_url = f"{urls['api']}bulk-delete/"
    payload = {"ids": [1, 2, 3, 4, 500, 501]}

    response = api_client.post(
        delete_url,
        headers=admin_headers,
        data=payload,
    )

    assert response.status_code == 400
    assert model.objects.count() == 304
    assert response.json()["details"] == "error qs message"


@pytest.mark.django_db
def test_delete_objects_not_deletable(
    admin_client: Client,
    model: type[Model],
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    mocker.patch(
        f"apps.{app_label}.views.{subapp_label}.ListView.deleter", new=CustomDeleter
    )

    payload = {
        "action-check": list(range(1, 10)),
        "kind": "action",
        "name": "delete",
    }

    response = admin_client.post(
        urls["index"],
        headers=headers_modal_GET,
        data=payload,
    )
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )

    assert response.status_code == 200
    assert messages_list[0].level == messages.ERROR
    assert messages_list[0].message == "error qs message"
    assert model.objects.count() == 304
