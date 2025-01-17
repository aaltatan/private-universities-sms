import pytest
from django.test import Client


@pytest.mark.django_db
def test_view_filter_simple_keyword_search(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?q=حم"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" in response.content.decode()
    assert "حمص" in response.content.decode()
    assert "ادلب" not in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 2


@pytest.mark.django_db
def test_view_filter_for_all_objects_contains_meta_letters(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?q=meta"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" not in response.content.decode()
    assert "حمص" in response.content.decode()
    assert "ادلب" in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 2


@pytest.mark.django_db
def test_view_filter_with_reversed_keywords(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?q=mena+language"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "ادلب" not in response.content.decode()
    assert "حماه" not in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "المنيا" in response.content.decode()
    assert response.context["page"].paginator.count == 1


@pytest.mark.django_db
def test_view_filter_all_objects_which_id_more_than_2(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?q=id > 2"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" not in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "ادلب" in response.content.decode()
    assert "المنيا" in response.content.decode()
    assert response.context["page"].paginator.count == 302


@pytest.mark.django_db
def test_view_filter_objects_which_id_more_than_2(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + '?q=id > 2 and name ~ "ل"'
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" not in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "ادلب" in response.content.decode()
    assert "المنيا" in response.content.decode()
    assert response.context["page"].paginator.count == 2


@pytest.mark.django_db
def test_view_filter_all_objects_which_id_in_one_or_three(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?q=id in (1, 3)"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "ادلب" in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 2


@pytest.mark.django_db
def test_view_filter_using_parts_of_words(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?q=منيا محافظ"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" not in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "ادلب" not in response.content.decode()
    assert "المنيا" in response.content.decode()
    assert response.context["page"].paginator.count == 1


@pytest.mark.django_db
def test_view_filter_with_name(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?name=حماه"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" in response.content.decode()
    assert "ادلب" not in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 1


@pytest.mark.django_db
def test_view_filter_with_description(
    super_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?description=meta"
    response = super_client.get(url)

    assert response.status_code == 200
    assert "حماه" not in response.content.decode()
    assert "حمص" in response.content.decode()
    assert "ادلب" in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 2
