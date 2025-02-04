import pytest
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser


@pytest.mark.django_db
def test_order(
    admin_client: Client,
    urls: dict[str, str],
    order_test_cases: tuple[str, list[tuple[int, str, str]]],
):
    querystring, data = order_test_cases
    url: str = urls["index"] + querystring

    response = admin_client.get(url)

    object_list = response.context["page"].object_list

    assert response.status_code == 200

    for idx, (id, name, description) in enumerate(data):

        if idx == 2:
            idx = -1

        assert object_list[idx].id == id
        assert object_list[idx].name == name
        assert object_list[idx].description == description


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_filters(
    admin_client: Client,
    urls: dict[str, str],
    filters_test_cases: tuple[str, int, tuple[tuple[str, int]]],
):
    querystring, results_count, data = filters_test_cases
    url: str = urls["index"] + querystring
    response = admin_client.get(url)

    assert response.status_code == 200

    for item in data:
        name, exists = item
        if exists:
            assert name in response.content.decode()
        else:
            assert name not in response.content.decode()

    assert response.context["page"].paginator.count == results_count


@pytest.mark.django_db
def test_api_filters(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    filters_test_cases: tuple[str, int, tuple[tuple[str, bool]]],
):
    querystring, results_count, data = filters_test_cases

    response: Response = api_client.get(
        path=urls["api"] + querystring,
        headers=admin_headers,
        format="json",
    )
    names = [item["name"] for item in response.json()["results"]]
    names = ", ".join(names)

    for item in data:
        name, exists = item
        if exists:
            assert name in names
        else:
            assert name not in names

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == results_count
