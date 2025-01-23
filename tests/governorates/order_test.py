import pytest
from django.test import Client
from selectolax.parser import HTMLParser


@pytest.mark.django_db
def test_view_filter_order_by_id_page_one(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?order_by=id"

    response = admin_client.get(url)

    assert response.status_code == 200
    assert response.context["page"].object_list[0].id == 1
    assert response.context["page"].object_list[1].id == 2
    assert response.context["page"].object_list[-1].id == 10
    assert response.context["page"].object_list[0].name == "محافظة حماه"
    assert response.context["page"].object_list[1].name == "محافظة حمص"
    assert response.context["page"].object_list[-1].name == "City 6"


@pytest.mark.django_db
def test_view_filter_order_by_id_page_twenty_one(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=21&order_by=id"

    response = admin_client.get(url)

    assert response.status_code == 200
    assert response.context["page"].object_list[0].id == 201
    assert response.context["page"].object_list[1].id == 202
    assert response.context["page"].object_list[-1].id == 210
    assert response.context["page"].object_list[0].name == "City 197"
    assert response.context["page"].object_list[1].name == "City 198"
    assert response.context["page"].object_list[-1].name == "City 206"


@pytest.mark.django_db
def test_view_filter_order_by_name_page_one(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?order_by=name"

    response = admin_client.get(url)

    assert response.status_code == 200
    assert response.context["page"].object_list[0].id == 1
    assert response.context["page"].object_list[1].id == 2
    assert response.context["page"].object_list[-1].id == 10
    assert response.context["page"].object_list[0].name == "محافظة حماه"
    assert response.context["page"].object_list[1].name == "محافظة حمص"
    assert response.context["page"].object_list[-1].name == "City 6"


@pytest.mark.django_db
def test_view_filter_order_by_name_page_twenty_one(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=21&order_by=name"

    response = admin_client.get(url)
    assert response.status_code == 200
    assert response.context["page"].object_list[0].id == 201
    assert response.context["page"].object_list[1].id == 202
    assert response.context["page"].object_list[-1].id == 210
    assert response.context["page"].object_list[0].name == "City 197"
    assert response.context["page"].object_list[1].name == "City 198"
    assert response.context["page"].object_list[-1].name == "City 206"


@pytest.mark.django_db
def test_view_filter_order_by_description_page_one(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?order_by=Description"

    response = admin_client.get(url)

    assert response.context["page"].object_list[0].description == "001"
    assert response.context["page"].object_list[1].description == "002"
    assert response.context["page"].object_list[-1].description == "010"
    assert response.context["page"].object_list[0].name == "City 300"
    assert response.context["page"].object_list[1].name == "City 299"
    assert response.context["page"].object_list[-1].name == "City 291"


@pytest.mark.django_db
def test_view_pagination(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=2"

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == 2
    assert len(rows) == 10


@pytest.mark.django_db
def test_pagination_with_invalid_page_number(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=dasd"

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == 1
    assert len(rows) == 10


@pytest.mark.django_db
def test_pagination_with_per_page(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=1&per_page=50"

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == 1
    assert len(rows) == 50


@pytest.mark.django_db
def test_pagination_with_per_page_all_and_invalid_page_number(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=dasd&per_page=all"

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == 1
    assert len(rows) == 304


@pytest.mark.django_db
def test_pagination_with_per_page_and_page_number_over_the_pages_count(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?page=12&per_page=100"

    response = admin_client.get(url)
    parser = HTMLParser(response.content)
    rows = parser.css("table tr:not(:first-child)")

    assert response.status_code == 200
    assert response.context["page"].number == 4
    assert len(rows) == 4
