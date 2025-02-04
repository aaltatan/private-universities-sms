import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status


@pytest.mark.django_db
def test_filters(
    admin_client: Client,
    urls: dict[str, str],
    filters_test_cases: tuple[str, int, tuple[tuple[str, bool]]],
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
def test_filter_objects_using_q(
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
