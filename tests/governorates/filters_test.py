import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status

from tests.utils import load_yaml


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["filters"],
)
def test_filters(admin_client: Client, urls: dict[str, str], params: dict):
    url: str = urls["index"] + params["querystring"]
    response = admin_client.get(url)

    assert response.status_code == 200

    for item in params["data"]:
        name, exists = item
        if exists:
            assert name in response.content.decode()
        else:
            assert name not in response.content.decode()

    assert response.context["page"].paginator.count == params["results_count"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["filters"],
)
def test_filter_objects_using_q(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    params: dict,
):
    response: Response = api_client.get(
        path=urls['api'] + params["querystring"],
        headers=admin_headers,
        format="json",
    )
    names = [item["name"] for item in response.json()["results"]]
    names = ", ".join(names)

    for item in params["data"]:
        name, exists = item
        if exists:
            assert name in names
        else:
            assert name not in names

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == params["results_count"]
