from typing import Any

from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser


class CommonQuerystringTests:
    @staticmethod
    def test_order(
        admin_client: Client,
        urls: dict[str, str],
        order_test_cases: tuple[str, tuple[int, ...]],
    ):
        querystring, ids = order_test_cases
        url: str = urls["index"] + querystring

        response = admin_client.get(url)

        object_list = response.context["page"].object_list

        assert response.status_code == 200

        for idx, id in enumerate(ids):
            if idx == 2:
                idx = -1

            assert object_list[idx].id == id

    @staticmethod
    def test_pagination(
        admin_client: Client,
        urls: dict[str, str],
        pagination_test_cases: tuple[str, int, str, str],
    ):
        querystring, count, next_page, prev_page = pagination_test_cases

        url: str = urls["index"] + querystring

        response = admin_client.get(url)
        parser = HTMLParser(response.content)
        rows = parser.css("table tr:not(:first-child)")

        res_next_page = parser.css_first(
            'button[title="Next Page"]',
        ).attributes.get("hx-get")

        res_prev_page = parser.css_first(
            'button[title="Previous Page"]',
        ).attributes.get("hx-get")

        if next_page is not None:
            assert res_next_page in next_page
        else:
            assert res_next_page == "?page="

        if prev_page is not None:
            assert res_prev_page in prev_page
        else:
            assert res_prev_page == "?page="

        assert response.status_code == 200
        assert len(rows) == count

    @staticmethod
    def test_api_pagination(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        pagination_test_cases: tuple[str, int, str, str],
        counts: dict[str, int],
    ):
        objects_count = counts["objects"]
        querystring, count, next_page, prev_page = pagination_test_cases
        response: Response = api_client.get(
            path=urls["api"] + querystring,
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["meta"]["results_count"] == objects_count
        assert len(response.json()["results"]) == count

        if next_page is not None:
            assert response.json()["links"]["next"].endswith(
                urls["api"] + next_page,
            )
        else:
            assert response.json()["links"]["next"] is None

        if prev_page is not None:
            assert response.json()["links"]["previous"].endswith(
                urls["api"] + prev_page
            )
        else:
            assert response.json()["links"]["previous"] is None

    @staticmethod
    def test_filters(
        admin_client: Client,
        urls: dict[str, str],
        filters_test_cases: tuple[str, int, str, tuple[Any, ...], tuple[Any, ...]],
    ):
        (
            querystring,
            results_count,
            required_field,
            exists_values,
            not_exists_values,
        ) = filters_test_cases
        url: str = urls["index"] + querystring
        response = admin_client.get(url)

        assert response.status_code == 200

        field_values_list = [
            getattr(n, required_field) for n in response.context["page"].object_list
        ]

        for value in exists_values:
            assert value in field_values_list

        for value in not_exists_values:
            assert value not in field_values_list

        assert response.context["page"].paginator.count == results_count

    @staticmethod
    def test_api_filters(
        api_client: APIClient,
        urls: dict[str, str],
        admin_headers: dict[str, str],
        filters_test_cases: tuple[str, int, str, tuple[Any, ...], tuple[Any, ...]],
    ):
        (
            querystring,
            results_count,
            required_field,
            exists_names,
            not_exists_names,
        ) = filters_test_cases

        response: Response = api_client.get(
            path=urls["api"] + querystring,
            headers=admin_headers,
            format="json",
        )
        field_values_list = [
            item[required_field] for item in response.json()["results"]
        ]
        field_values_list = ", ".join(field_values_list)

        for value in exists_names:
            assert value in field_values_list

        for value in not_exists_names:
            assert value not in field_values_list

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["meta"]["results_count"] == results_count
