import pytest
from django.test import Client
from selectolax.parser import HTMLParser


@pytest.mark.django_db
@pytest.mark.parametrize(
    "querystring,expected_ids,expected_names,expected_descriptions",
    [
        (
            "?order_by=Id",
            [1, 2, 10],
            ["محافظة حماه", "محافظة حمص", "City 006"],
            ["goo", "meta", "006"],
        ),
        (
            "?page=21&order_by=Id",
            [201, 202, 210],
            ["City 197", "City 198", "City 206"],
            ["197", "198", "206"],
        ),
        (
            "?page=1&order_by=-Id",
            [304, 303, 295],
            ["City 300", "City 299", "City 291"],
            ["300", "299", "291"],
        ),
        (
            "?order_by=Name",
            [5, 6, 14],
            ["City 001", "City 002", "City 010"],
            ["001", "002", "010"],
        ),
        (
            "?order_by=Description",
            [5, 6, 14],
            ["City 001", "City 002", "City 010"],
            ["001", "002", "010"],
        ),
        (
            "?page=21&order_by=Name",
            [205, 206, 214],
            ["City 201", "City 202", "City 210"],
            ["201", "202", "210"],
        ),
    ],
)
def test_view_order(
    admin_client: Client,
    urls: dict[str, str],
    querystring: str,
    expected_ids: list[int],
    expected_names: list[str],
    expected_descriptions: list[str],
):
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
