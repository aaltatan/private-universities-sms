import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from tests.utils import load_yaml


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["order"],
)
def test_view_order(
    admin_client: Client,
    urls: dict[str, str],
    params: dict,
):
    url: str = urls["index"] + params["querystring"]

    response = admin_client.get(url)

    object_list = response.context["page"].object_list

    assert response.status_code == 200
    assert object_list[0].id == params["expected_ids"][0]
    assert object_list[1].id == params["expected_ids"][1]
    assert object_list[-1].id == params["expected_ids"][2]
    assert object_list[0].name == params["expected_names"][0]
    assert object_list[1].name == params["expected_names"][1]
    assert object_list[-1].name == params["expected_names"][2]
    assert object_list[0].description == params["expected_descriptions"][0]
    assert object_list[1].description == params["expected_descriptions"][1]
    assert object_list[-1].description == params["expected_descriptions"][2]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "querystring,rows_count,page_number",
    [
        pytest.param("?page=2", 10, 2),
        pytest.param("?page=dasd", 10, 1),
        pytest.param("?page=21&per_page=50", 4, 7),
        pytest.param("?page=12&per_page=100", 4, 4),
        pytest.param("?page=dasd&per_page=all", 304, 1, marks=pytest.mark.slow),
    ],
)
def test_view_pagination(
    admin_client: Client,
    urls: dict[str, str],
    querystring: str,
    rows_count: int,
    page_number: int,
):
    url: str = urls["index"] + querystring

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == page_number
    assert len(rows) == rows_count
