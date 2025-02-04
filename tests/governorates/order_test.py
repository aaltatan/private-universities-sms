import pytest
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser


@pytest.mark.django_db
def test_view_order(
    admin_client: Client,
    urls: dict[str, str],
    order_test_cases: tuple[str, list[int], list[str], list[str]],
):
    (
        querystring,
        expected_ids,
        expected_names,
        expected_descriptions,
    ) = order_test_cases
    url: str = urls["index"] + querystring

    response = admin_client.get(url)

    object_list = response.context["page"].object_list

    assert response.status_code == 200
    assert object_list[0].id == expected_ids[0]
    assert object_list[1].id == expected_ids[1]
    assert object_list[-1].id == expected_ids[2]
    assert object_list[0].name == expected_names[0]
    assert object_list[1].name == expected_names[1]
    assert object_list[-1].name == expected_names[2]
    assert object_list[0].description == expected_descriptions[0]
    assert object_list[1].description == expected_descriptions[1]
    assert object_list[-1].description == expected_descriptions[2]


@pytest.mark.django_db
def test_view_pagination(
    admin_client: Client,
    urls: dict[str, str],
    pagination_test_cases: tuple[str, int, int],
):
    querystring, rows_count, page_number = pagination_test_cases
    url: str = urls["index"] + querystring

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == page_number
    assert len(rows) == rows_count


@pytest.mark.django_db
def test_api_pagination(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    api_pagination_test_cases: tuple[str, int, str, str],
):
    query_string, count, next_page, prev_page = api_pagination_test_cases
    response: Response = api_client.get(
        path=urls["api"] + query_string,
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 304
    assert len(response.json()["results"]) == count

    if next_page is not None:
        assert response.json()["next"].endswith(urls["api"] + next_page)
    else:
        assert response.json()["next"] is None

    if prev_page is not None:
        assert response.json()["previous"].endswith(urls["api"] + prev_page)
    else:
        assert response.json()["previous"] is None
