import json

import pytest
import pytest_mock
from django.contrib import messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model
from apps.core.utils import Deleter


class CommonDeleteTests:
    @staticmethod
    def test_delete_object(
        model: type[Model],
        admin_client: Client,
        urls: dict[str, str],
        headers_modal_GET: dict[str, str],
        counts: dict[str, int],
    ) -> None:
        obj = model.objects.first()
        response = admin_client.post(
            obj.get_delete_url(),
            headers=headers_modal_GET,
        )
        location = json.loads(
            response.headers.get("Hx-Location", {}),
        )
        location_path = location.get("path", "")
        messages_list = list(
            messages.get_messages(response.wsgi_request),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert location_path == urls["index"]
        assert response.headers.get("Hx-Trigger") == "messages"
        assert messages_list[0].level == messages.SUCCESS
        assert messages_list[0].message == f"{obj.name} has been deleted successfully."
        assert model.objects.count() == counts["objects"] - 1

    @staticmethod
    def test_delete_when_no_deleter_class_is_defined(
        admin_client: Client,
        model: type[Model],
        headers_modal_GET: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
    ):
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.DeleteView.deleter", new=None
        )
        obj = model.objects.first()
        with pytest.raises(AttributeError):
            admin_client.post(
                obj.get_delete_url(),
                headers=headers_modal_GET,
            )

    @staticmethod
    def test_delete_when_deleter_class_is_not_subclass_of_Deleter(
        admin_client: Client,
        model: type[Model],
        headers_modal_GET: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
    ):
        class Deleter:
            pass

        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.DeleteView.deleter", new=Deleter
        )
        obj = model.objects.first()
        with pytest.raises(TypeError):
            admin_client.post(
                obj.get_delete_url(),
                headers=headers_modal_GET,
            )

    @staticmethod
    def test_api_delete_object(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        model: type[Model],
        counts: dict[str, int],
    ):
        for idx in range(1, 11):
            response: Response = api_client.delete(
                path=f"{urls['api']}{idx}/",
                headers=admin_headers,
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

        assert model.objects.count() == counts["objects"] - 10

    @staticmethod
    def test_delete_object_with_invalid_id(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        model: type[Model],
        model_name: str,
        counts: dict[str, int],
    ):
        objects_count = counts["objects"]
        response: Response = api_client.get(
            path=f"{urls['api']}312312",
            headers=admin_headers,
            follow=True,
        )
        assert response.json() == {
            "detail": f"No {model_name} matches the given query."
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert model.objects.count() == objects_count

    @staticmethod
    def test_delete_and_bulk_delete_object_when_deleter_class_is_None(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
    ):
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.APIViewSet.deleter", new=None
        )

        with pytest.raises(AttributeError):
            api_client.delete(
                path=f"{urls['api']}1/",
                headers=admin_headers,
            )

        with pytest.raises(AttributeError):
            api_client.post(
                path=f"{urls['api']}bulk-delete/",
                data={"ids": [1, 2, 3, 4, 500, 501]},
                headers=admin_headers,
            )

    @staticmethod
    def test_delete_and_bulk_delete_object_when_deleter_class_is_not_a_subclass_of_Deleter(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
    ):
        class Deleter:
            pass

        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.APIViewSet.deleter", new=Deleter
        )

        with pytest.raises(TypeError):
            api_client.delete(
                path=f"{urls['api']}1/",
                headers=admin_headers,
            )

        with pytest.raises(TypeError):
            api_client.post(
                path=f"{urls['api']}bulk-delete/",
                data={"ids": [1, 2, 3, 4, 500, 501]},
                headers=admin_headers,
            )

    @staticmethod
    def test_delete_object_not_deletable(
        admin_client: Client,
        model: type[Model],
        headers_modal_GET: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
        counts: dict[str, int],
        custom_deleter: type[Deleter],
    ):
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.DeleteView.deleter",
            new=custom_deleter,
        )

        delete_url = model.objects.order_by("id").first().get_delete_url()
        response = admin_client.post(delete_url, headers=headers_modal_GET)
        messages_list = list(
            messages.get_messages(request=response.wsgi_request),
        )

        assert response.status_code == 200
        assert messages_list[0].level == messages.ERROR
        assert messages_list[0].message == "error obj message"
        assert model.objects.count() == counts["objects"]

    @staticmethod
    def test_api_delete_object_not_deletable(
        api_client: APIClient,
        admin_headers: dict[str, str],
        urls: dict[str, str],
        model: type[Model],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
        counts: dict[str, int],
        custom_deleter: type[Deleter],
    ):
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.APIViewSet.deleter",
            new=custom_deleter,
        )

        delete_url = f"{urls['api']}1/"

        response = api_client.delete(delete_url, headers=admin_headers)

        assert response.status_code == 400
        assert model.objects.count() == counts["objects"]
        assert response.json()["details"] == "error obj message"

    @staticmethod
    def test_api_delete_objects_not_deletable(
        api_client: APIClient,
        admin_headers: dict[str, str],
        urls: dict[str, str],
        model: type[Model],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
        counts: dict[str, int],
        custom_deleter: type[Deleter],
    ):
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.APIViewSet.deleter",
            new=custom_deleter,
        )

        delete_url = f"{urls['api']}bulk-delete/"
        payload = {"ids": [1, 2, 3, 4, 500, 501]}

        response = api_client.post(
            delete_url,
            headers=admin_headers,
            data=payload,
        )

        assert response.status_code == 400
        assert model.objects.count() == counts["objects"]
        assert response.json()["details"] == "error qs message"

    @staticmethod
    def test_delete_objects_not_deletable(
        admin_client: Client,
        model: type[Model],
        urls: dict[str, str],
        headers_modal_GET: dict[str, str],
        mocker: pytest_mock.MockerFixture,
        app_label: str,
        subapp_label: str,
        counts: dict[str, int],
        custom_deleter: type[Deleter],
    ):
        mocker.patch(
            f"apps.{app_label}.views.{subapp_label}.ListView.deleter",
            new=custom_deleter,
        )

        payload = {
            "action_check": list(range(1, 10)),
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
        assert model.objects.count() == counts["objects"]
