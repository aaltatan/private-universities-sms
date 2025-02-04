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


@pytest.mark.django_db
def test_api_pagination(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    pagination_test_cases: tuple[str, int, str, str],
):
    querystring, count, next_page, prev_page = pagination_test_cases
    response: Response = api_client.get(
        path=urls["api"] + querystring,
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
