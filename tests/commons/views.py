import re

import pytest
from django.contrib import messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.constants import PERMISSION
from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used, parse_buttons


class CommonViewsTests:
    @staticmethod
    def test_api_read_objects(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        counts: dict[str, int],
    ):
        response: Response = api_client.get(
            path=urls["api"],
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["meta"]["results_count"] == counts["objects"]
        assert len(response.json()["results"]) == 10

    @staticmethod
    def test_api_read_object(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        api_keys: list[str],
    ):
        response: Response = api_client.get(
            path=f"{urls['api']}1/",
            headers=admin_headers,
        )
        assert response.status_code == 200

        for key in api_keys:
            assert key in response.json()

    @staticmethod
    def test_api_read_object_with_invalid_id(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
    ):
        response: Response = api_client.get(
            path=f"{urls['api']}4123/",
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @staticmethod
    def test_response_bulk_delete_modal(
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

    @staticmethod
    def test_response_create_from_modal_without_using_target_in_hx_request(
        admin_client: Client,
        urls: dict[str, str],
        headers_modal_GET: dict[str, str],
    ) -> None:
        with pytest.raises(ValueError, match="target is required"):
            admin_client.get(urls["create"], headers=headers_modal_GET)

    @staticmethod
    def test_response_access_create_page(
        admin_client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
    ) -> None:
        response = admin_client.get(urls["create"])

        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["create"], response)

    @staticmethod
    def test_response_delete_object_if_headers_has_no_hx_request(
        admin_client: Client, model: type[Model]
    ) -> None:
        obj = model.objects.first()
        response = admin_client.post(
            obj.get_delete_url(),
        )
        messages_list = list(
            messages.get_messages(response.wsgi_request),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert messages_list[0].level == messages.ERROR
        assert (
            messages_list[0].message
            == "you can't delete this object because you are not using htmx."
        )

    @staticmethod
    def test_response_delete_modal_without_using_htmx(
        model: type[Model], admin_client: Client
    ) -> None:
        obj = model.objects.first()
        response = admin_client.get(obj.get_delete_url())
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @staticmethod
    def test_response_delete_modal_with_using_htmx(
        model: type[Model],
        admin_client: Client,
        templates: dict[str, str],
        headers_modal_GET: dict[str, str],
    ) -> None:
        obj = model.objects.first()

        response = admin_client.get(
            obj.get_delete_url(),
            headers=headers_modal_GET,
        )
        parser = HTMLParser(response.content)
        modal_body = parser.css_first(
            "#modal-container p",
        ).text(strip=True)

        modal_body = re.sub(r"\s+", " ", modal_body)

        assert modal_body == f"are you sure you want to delete {obj.name} ?"
        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["delete_modal"], response)

    @staticmethod
    def test_response_index_has_right_columns(
        admin_client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
        index_columns: list[str],
    ):
        response = admin_client.get(urls["index"])
        parser = HTMLParser(response.content)
        ths = parser.css("th[scope='col']")
        ths = [th.text(strip=True).lower() for th in ths]

        assert response.status_code == 200
        assert len(ths) == len(index_columns) + 1  # checkbox column
        assert is_template_used(templates["index"], response)

        for column in index_columns:
            assert column in ths

    @staticmethod
    def test_response_index_GET_with_htmx(
        admin_client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
    ):
        headers = {
            "HX-Request": "true",
        }
        response = admin_client.get(urls["index"], headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["table"], response)

    @staticmethod
    def test_response_index_has_checkboxes_admin(
        admin_client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
    ):
        response = admin_client.get(urls["index"])
        parser = HTMLParser(response.content)
        checkboxes = parser.css("input[id^='row-check-']")

        assert len(checkboxes) == 10
        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["index"], response)

    @staticmethod
    def test_response_index_has_checkboxes_with_view_delete_perms(
        client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
        subapp_label: str,
    ):
        client.login(
            username=f"{subapp_label}_user_with_view_delete_perm",
            password="password",
        )
        response = client.get(urls["index"])
        parser = HTMLParser(response.content)
        checkboxes = parser.css("input[id^='row-check-']")

        assert response.status_code == status.HTTP_200_OK
        assert len(checkboxes) == 10
        assert is_template_used(templates["index"], response)

    @staticmethod
    def test_response_index_has_no_checkboxes_with_no_permission(
        client: Client,
        urls: dict[str, str],
        templates: dict[str, str],
        subapp_label: str,
    ):
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )
        response = client.get(urls["index"])
        parser = HTMLParser(response.content)
        checkboxes = parser.css("input[id^='row-check-']")

        assert len(checkboxes) == 0
        assert response.status_code == status.HTTP_200_OK
        assert is_template_used(templates["index"], response)

    @staticmethod
    def test_response_view_has_all_html_elements_which_need_permissions(
        admin_client: Client, urls: dict[str, str]
    ):
        response = admin_client.get(urls["index"])
        parser = HTMLParser(response.content)
        buttons = parse_buttons(parser)

        assert buttons["add_btn_exists"]
        assert buttons["export_btn_exists"]
        assert buttons["activities_btn_exists"]
        assert buttons["delete_btn_exists"]
        assert buttons["edit_btn_exists"]
        assert buttons["delete_all_btn_exists"]
        assert buttons["activities_btn_exists"]

    @staticmethod
    def test_response_view_user_has_view_permissions(
        client: Client,
        urls: dict[str, str],
        subapp_label: str,
    ):
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )

        response = client.get(urls["index"])
        parser = HTMLParser(response.content)
        buttons = parse_buttons(parser)

        assert response.status_code == status.HTTP_200_OK
        assert buttons["add_btn_exists"] is False
        assert buttons["delete_btn_exists"] is False
        assert buttons["delete_all_btn_exists"] is False
        assert buttons["edit_btn_exists"] is False
        assert buttons["export_btn_exists"] is False

    @staticmethod
    def test_response_view_buttons_does_exists(
        client: Client,
        urls: dict[str, str],
        subapp_label: str,
        buttons_test_cases: tuple[PERMISSION, tuple[tuple[str, int], ...]],
    ):
        perm, buttons = buttons_test_cases
        client.login(
            username=f"{subapp_label}_user_with_view_{perm}_perm",
            password="password",
        )
        response = client.get(urls["index"])
        parser = HTMLParser(response.content)
        res_buttons = parse_buttons(parser)

        assert response.status_code == status.HTTP_200_OK
        for key, exists in buttons:
            exists = bool(exists)
            assert res_buttons[key] is exists

    @staticmethod
    @pytest.mark.django_db
    def test_response_update_without_using_target_in_hx_request(
        admin_client: Client,
        model: type[Model],
        headers_modal_GET: dict[str, str],
    ) -> None:
        with pytest.raises(ValueError):
            admin_client.get(
                model.objects.first().get_update_url(),
                headers=headers_modal_GET,
            )

    @staticmethod
    @pytest.mark.django_db
    def test_response_index_page_has_update_links_for_authorized_user(
        admin_client: Client,
        urls: dict[str, str],
        model: type[Model],
    ) -> None:
        response = admin_client.get(urls["index"])
        parser = HTMLParser(response.content)
        tds_name = parser.css("td[data-header='name'] a")
        tds_id = parser.css("span[aria-label='object id']")
        context_menu_btns = parser.css("table li[role='menuitem']")

        assert response.status_code == status.HTTP_200_OK
        assert len(tds_name) == 10
        assert len(context_menu_btns) == 20

        for pk, td in zip(tds_id, tds_name):
            pk = int(pk.attributes["data-id"])
            update_url = model.objects.get(pk=pk).get_update_url()
            assert update_url == td.attributes["href"]
