import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.parametrize(
    "querystring,data,page_number",
    [
        (
            "?q=حم",
            [
                {"name": "حماه", "exists": True},
                {"name": "حمص", "exists": True},
                {"name": "ادلب", "exists": False},
                {"name": "المنيا", "exists": False},
            ],
            2,
        ),
        (
            "?q=meta",
            [
                {"name": "حماه", "exists": False},
                {"name": "حمص", "exists": True},
                {"name": "ادلب", "exists": True},
                {"name": "المنيا", "exists": False},
            ],
            2,
        ),
        (
            "?q=mena+language",
            [
                {"name": "ادلب", "exists": False},
                {"name": "حماه", "exists": False},
                {"name": "حمص", "exists": False},
                {"name": "المنيا", "exists": True},
            ],
            1,
        ),
        (
            "?q=id > 2",
            [
                {"name": "حماه", "exists": False},
                {"name": "حمص", "exists": False},
                {"name": "ادلب", "exists": True},
                {"name": "المنيا", "exists": True},
            ],
            302,
        ),
        (
            "?q=id > 2 and name ~ 'ل'",
            [
                {"name": "حماه", "exists": False},
                {"name": "حمص", "exists": False},
                {"name": "ادلب", "exists": True},
                {"name": "المنيا", "exists": True},
            ],
            2,
        ),
        (
            "?q=id in (1, 3)",
            [
                {"name": "حماه", "exists": True},
                {"name": "حمص", "exists": False},
                {"name": "ادلب", "exists": True},
                {"name": "المنيا", "exists": False},
            ],
            2,
        ),
        (
            "?q=منيا محافظ",
            [
                {"name": "حماه", "exists": False},
                {"name": "حمص", "exists": False},
                {"name": "ادلب", "exists": False},
                {"name": "المنيا", "exists": True},
            ],
            1,
        ),
    ],
)
def test_view_filter_simple_keyword_search(
    admin_client: Client,
    urls: dict[str, str],
    querystring: str,
    data: list[dict[str, str | bool]],
    page_number: int,
):
    url: str = urls["index"] + querystring
    response = admin_client.get(url)

    assert response.status_code == 200
    for item in data:
        if item["exists"]:
            assert item["name"] in response.content.decode()
        else:
            assert item["name"] not in response.content.decode()
    assert response.context["page"].paginator.count == page_number


# @pytest.mark.django_db
# def test_view_filter_for_all_objects_contains_meta_letters(
#     admin_client: Client,
#     urls: dict[str, str],
# ):
#     url: str = urls["index"] + "?q=meta"
#     response = admin_client.get(url)

#     assert response.status_code == 200
#     assert "حماه" not in response.content.decode()
#     assert "حمص" in response.content.decode()
#     assert "ادلب" in response.content.decode()
#     assert "المنيا" not in response.content.decode()
#     assert response.context["page"].paginator.count == 2


# @pytest.mark.django_db
# def test_view_filter_with_reversed_keywords(
#     admin_client: Client,
#     urls: dict[str, str],
# ):
#     url: str = urls["index"] + "?q=mena+language"
#     response = admin_client.get(url)

#     assert response.status_code == 200
#     assert "ادلب" not in response.content.decode()
#     assert "حماه" not in response.content.decode()
#     assert "حمص" not in response.content.decode()
#     assert "المنيا" in response.content.decode()
#     assert response.context["page"].paginator.count == 1


# @pytest.mark.django_db
# def test_view_filter_all_objects_which_id_more_than_2(
#     admin_client: Client,
#     urls: dict[str, str],
# ):
#     url: str = urls["index"] + "?q=id > 2"
#     response = admin_client.get(url)

#     assert response.status_code == 200
#     assert "حماه" not in response.content.decode()
#     assert "حمص" not in response.content.decode()
#     assert "ادلب" in response.content.decode()
#     assert "المنيا" in response.content.decode()
#     assert response.context["page"].paginator.count == 302


# @pytest.mark.django_db
# def test_view_filter_objects_which_id_more_than_2(
#     admin_client: Client,
#     urls: dict[str, str],
# ):
#     url: str = urls["index"] + '?q=id > 2 and name ~ "ل"'
#     response = admin_client.get(url)

#     assert response.status_code == 200
#     assert "حماه" not in response.content.decode()
#     assert "حمص" not in response.content.decode()
#     assert "ادلب" in response.content.decode()
#     assert "المنيا" in response.content.decode()
#     assert response.context["page"].paginator.count == 2


# @pytest.mark.django_db
# def test_view_filter_all_objects_which_id_in_one_or_three(
#     admin_client: Client,
#     urls: dict[str, str],
# ):
#     url: str = urls["index"] + "?q=id in (1, 3)"
#     response = admin_client.get(url)

#     assert response.status_code == 200
#     assert "حماه" in response.content.decode()
#     assert "حمص" not in response.content.decode()
#     assert "ادلب" in response.content.decode()
#     assert "المنيا" not in response.content.decode()
#     assert response.context["page"].paginator.count == 2


# @pytest.mark.django_db
# def test_view_filter_using_parts_of_words(
#     admin_client: Client,
#     urls: dict[str, str],
# ):
#     url: str = urls["index"] + "?q=منيا محافظ"
#     response = admin_client.get(url)

#     assert response.status_code == 200
#     assert "حماه" not in response.content.decode()
#     assert "حمص" not in response.content.decode()
#     assert "ادلب" not in response.content.decode()
#     assert "المنيا" in response.content.decode()
#     assert response.context["page"].paginator.count == 1


@pytest.mark.django_db
def test_view_filter_with_name(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?name=حماه"
    response = admin_client.get(url)

    assert response.status_code == 200
    assert "حماه" in response.content.decode()
    assert "ادلب" not in response.content.decode()
    assert "حمص" not in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 1


@pytest.mark.django_db
def test_view_filter_with_description(
    admin_client: Client,
    urls: dict[str, str],
):
    url: str = urls["index"] + "?description=meta"
    response = admin_client.get(url)

    assert response.status_code == 200
    assert "حماه" not in response.content.decode()
    assert "حمص" in response.content.decode()
    assert "ادلب" in response.content.decode()
    assert "المنيا" not in response.content.decode()
    assert response.context["page"].paginator.count == 2
