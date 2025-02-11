import json

import pytest
import pytest_mock
from django.contrib import messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model


class CommonActionsTests:
    @staticmethod
    def test_bulk_delete(
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
            == f"{counts['bulk_delete_batch']} selected objects have been deleted successfully."
        )
        assert model.objects.count() == objects_count - bulk_delete_batch

    @staticmethod
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

    @staticmethod
    def test_bulk_delete_when_no_deleter_class_is_defined(
        admin_client: Client,
        urls: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
        counts: dict[str, int],
    ):
        bulk_delete_batch = counts["bulk_delete_batch"]
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.ListView.deleter", new=None
        )
        data: dict = {
            "action-check": list(range(1, bulk_delete_batch + 1)),
            "kind": "action",
            "name": "delete",
        }
        with pytest.raises(AttributeError):
            admin_client.post(urls["index"], data)

    @staticmethod
    def test_bulk_delete_when_deleter_class_is_not_subclass_of_Deleter(
        admin_client: Client,
        urls: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
        counts: dict[str, int],
    ):
        bulk_delete_batch = counts["bulk_delete_batch"]

        class Deleter:
            pass

        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.ListView.deleter", new=Deleter
        )
        data: dict = {
            "action-check": list(range(1, bulk_delete_batch + 1)),
            "kind": "action",
            "name": "delete",
        }
        with pytest.raises(TypeError):
            admin_client.post(urls["index"], data)

    @staticmethod
    def test_bulk_delete_api(
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
