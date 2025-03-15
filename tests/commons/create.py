from typing import Any

import pytest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


class CommonCreateTests:
    @staticmethod
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

    @staticmethod
    def test_create_new_object_with_save_and_continue_editing_btn(
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

        clean_data_sample["save_and_continue_editing"] = "true"
        response = admin_client.post(urls["create"], clean_data_sample)
        messages_list = list(
            get_messages(request=response.wsgi_request),
        )
        success_message = f"{clean_data_sample['name']} has been created successfully"

        last_obj = model.objects.all().order_by("id").last()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers.get("Hx-Redirect") == last_obj.get_update_url()
        assert response.headers.get("Hx-Trigger") == "messages"
        assert messages_list[0].level == messages.SUCCESS
        assert messages_list[0].message == success_message
        assert model.objects.count() == objects_count + 1

    @staticmethod
    def test_create_from_modal_without_using_save_or_save_and_add_another(
        admin_client: Client,
        urls: dict[str, str],
        headers_modal_GET: dict[str, str],
        clean_data_sample: dict[str, str],
    ) -> None:
        headers = {**headers_modal_GET, "target": "#modal-container"}
        with pytest.raises(
            ValueError,
            match="save, save_and_add_another or save_and_continue_editing is required",
        ):
            admin_client.post(urls["create"], clean_data_sample, headers=headers)

    @staticmethod
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

    @staticmethod
    def test_create_new_object_with_dirty_or_duplicated_data(
        admin_client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
        model: type[Model],
        dirty_data_test_cases: tuple[dict[str, str], list[str]],
        counts: dict[str, int],
    ) -> None:
        objects_count = counts["objects"]
        data, errors = dirty_data_test_cases
        data["save"] = "true"
        response = admin_client.get(urls["create"])

        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["create"], response)

        response = admin_client.post(urls["create"], data)
        parser = HTMLParser(response.content)
        form_hx_post = parser.css_first("form[hx-post]").attributes.get("hx-post")

        errors_el = parser.css(
            "form ul[aria-label='errors list'] span[aria-label='error']"
        )

        for error in errors:
            assert error in [e.text(strip=True) for e in errors_el]

        assert is_template_used(templates["create_form"], response)
        assert response.status_code == status.HTTP_200_OK
        assert form_hx_post == urls["create"]
        assert model.objects.count() == objects_count

    @staticmethod
    def test_create_new_object_with_modal_with_dirty_or_duplicated_data(
        admin_client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
        model: type[Model],
        dirty_data_test_cases: tuple[dict[str, Any], list[str]],
        headers_modal_GET: dict[str, str],
        subapp_label: str,
        counts: dict[str, int],
    ) -> None:
        objects_count = counts["objects"]
        data, errors = dirty_data_test_cases
        data["save"] = "true"
        url = urls["create"] + "?per_page=10&ordering=-name"
        headers = {
            **headers_modal_GET,
            "target": "#modal-container",
        }
        response = admin_client.get(url, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["create_modal_form"], response)

        headers = {
            **headers,
            "target": f"{subapp_label}-table",
            "dont-redirect": "true",
        }

        response = admin_client.post(urls["create"], data, headers=headers)
        parser = HTMLParser(response.content)
        form_hx_post = parser.css_first("form[hx-post]").attributes.get(
            "hx-post",
        )
        errors_el = parser.css(
            "form ul[aria-label='errors list'] span[aria-label='error']"
        )

        for error in errors:
            assert error in [e.text(strip=True) for e in errors_el]

        assert is_template_used(templates["create_modal_form"], response)
        assert response.status_code == status.HTTP_200_OK
        assert form_hx_post == urls["create"]
        assert model.objects.count() == objects_count

    @staticmethod
    def test_create_api_object_with_dirty_data(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        dirty_data_api_test_cases: tuple[dict[str, Any], dict[str, list[str]]],
    ):
        data, error = dirty_data_api_test_cases
        response: Response = api_client.post(
            path=urls["api"], data=data, headers=admin_headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == error
