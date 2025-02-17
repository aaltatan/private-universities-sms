from typing import Any

from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


class CommonUpdateTests:
    @staticmethod
    def test_update_with_dirty_data(
        admin_client: Client,
        model: type[Model],
        dirty_data_test_cases: tuple[dict[str, str], list[str]],
        templates: dict[str, str],
        counts: dict[str, int],
    ):
        data, errors = dirty_data_test_cases
        obj = model.objects.first()
        url = obj.get_update_url()

        response = admin_client.post(url, data)
        parser = HTMLParser(response.content)
        errors_el = parser.css(
            "form ul[aria-label='errors list'] span[aria-label='error']",
        )

        for error in errors:
            assert error in [e.text(strip=True) for e in errors_el]
        assert is_template_used(templates["update_form"], response)
        assert response.status_code == status.HTTP_200_OK

        assert model.objects.count() == counts["objects"]

    @staticmethod
    def test_update_with_modal_with_dirty_data(
        admin_client: Client,
        model: type[Model],
        dirty_data_test_cases: tuple[dict[str, str], list[str]],
        templates: dict[str, str],
        headers_modal_GET: dict[str, str],
        subapp_label: str,
        counts: dict[str, int],
    ):
        data, errors = dirty_data_test_cases
        obj = model.objects.first()
        url = obj.get_update_url() + "?page=1&per_page=10&ordering=-id"

        headers = {
            **headers_modal_GET,
            "target": f"#{subapp_label}-table",
        }

        response = admin_client.post(url, data, headers=headers)
        parser = HTMLParser(response.content)
        errors_el = parser.css(
            "form ul[aria-label='errors list'] span[aria-label='error']",
        )

        for error in errors:
            assert error in [e.text(strip=True) for e in errors_el]

        assert is_template_used(templates["update_modal_form"], response)
        assert response.status_code == status.HTTP_200_OK

        assert model.objects.count() == counts["objects"]

    @staticmethod
    def test_update_object_with_dirty_data(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        dirty_data_api_test_cases: tuple[dict[str, Any], dict[str, list[str]]],
    ):
        data, expected_response = dirty_data_api_test_cases
        response: Response = api_client.put(
            path=f"{urls['api']}3/", data=data, headers=admin_headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response
