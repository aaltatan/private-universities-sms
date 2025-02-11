from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model


class CommonPermissionsTests:
    @staticmethod
    def test_bulk_delete_without_permissions(
        client: Client,
        urls: dict[str, str],
        subapp_label: str,
        counts: dict[str, int],
    ):
        bulk_delete_batch = counts["bulk_delete_batch"]
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )

        data: dict = {
            "action-check": list(range(1, bulk_delete_batch + 1)),
            "kind": "action",
            "name": "delete",
        }

        response = client.post(urls["index"], data, follow=True)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_bulk_delete_with_permissions_only_for_view(
        client: Client,
        urls: dict[str, str],
        subapp_label: str,
        counts: dict[str, int],
    ):
        bulk_delete_batch = counts["bulk_delete_batch"]
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )

        data: dict = {
            "action-check": list(range(1, bulk_delete_batch + 1)),
            "kind": "action",
            "name": "delete",
        }

        response = client.post(urls["index"], data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_create_object_api_without_permissions(
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

    @staticmethod
    def test_access_create_page_without_permission(
        client: Client, urls: dict[str, str], subapp_label: str
    ) -> None:
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )
        response = client.get(urls["create"])
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_access_update_page_without_permission(
        client: Client, subapp_label: str, model: type[Model]
    ) -> None:
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )
        update_url = model.objects.first().get_update_url()
        response = client.get(update_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_access_index_without_permissions(
        client: Client,
        urls: dict[str, str],
    ):
        client.login(
            username="user_with_no_perm",
            password="password",
        )

        response = client.get(urls["index"])
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_api_read_objects_without_permissions(
        api_client: APIClient, urls: dict[str, str], user_headers: dict[str, str]
    ):
        response: Response = api_client.get(
            path=urls["api"],
            headers=user_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_api_read_object_without_permissions(
        api_client: APIClient,
        urls: dict[str, str],
        user_headers: dict[str, str],
    ):
        response: Response = api_client.get(
            path=f"{urls['api']}1/",
            headers=user_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @staticmethod
    def test_index_page_has_no_update_links_for_unauthorized_user(
        client: Client,
        urls: dict[str, str],
        model: type[Model],
        subapp_label: str,
    ) -> None:
        client.login(
            username=f"{subapp_label}_user_with_view_delete_perm",
            password="password",
        )
        response = client.get(urls["index"])

        parser = HTMLParser(response.content)

        tds_name = parser.css("td[data-header='name']")
        tds_name_href = parser.css("td[data-header='name'] a")
        delete_context_menu_btns = parser.css("table li[role='menuitem']")
        update_response = client.get(model.objects.first().get_update_url())

        assert response.status_code == status.HTTP_200_OK
        assert len(tds_name_href) == 0

        for pk, td in enumerate(tds_name, 1):
            update_url = model.objects.get(pk=pk).name
            assert update_url == td.text(strip=True)

        assert len(delete_context_menu_btns) == 10
        assert update_response.status_code == status.HTTP_403_FORBIDDEN
