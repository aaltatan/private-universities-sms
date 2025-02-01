import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.parametrize(
    "querystring,data,page_number",
    [
        (
            "?q=حم",
            [("حماه", True), ("حمص", True), ("ادلب", False), ("المنيا", False)],
            2,
        ),
        (
            "?q=meta",
            [("حماه", False), ("حمص", True), ("ادلب", True), ("المنيا", False)],
            2,
        ),
        (
            "?q=mena+language",
            [("حماه", False), ("حمص", False), ("ادلب", False), ("المنيا", True)],
            1,
        ),
        (
            "?q=id > 2",
            [("حماه", False), ("حمص", False), ("ادلب", True), ("المنيا", True)],
            302,
        ),
        (
            '?q=id > 2 and name ~ "ل"',
            [("حماه", False), ("حمص", False), ("ادلب", True), ("المنيا", True)],
            2,
        ),
        (
            "?q=id > 2 and name ~ 'ل'", # using ' instead of "
            [("حماه", False), ("حمص", False), ("ادلب", False), ("المنيا", False)],
            0,
        ),
        (
            "?q=id in (1, 3)",
            [("حماه", True), ("حمص", False), ("ادلب", True), ("المنيا", False)],
            2,
        ),
        (
            "?q=منيا محافظ",
            [("حماه", False), ("حمص", False), ("ادلب", False), ("المنيا", True)],
            1,
        ),
        (
            "?name=حماه",
            [("حماه", True), ("حمص", False), ("ادلب", False), ("المنيا", False)],
            1,
        ),
        (
            "?description=meta",
            [("حماه", False), ("حمص", True), ("ادلب", True), ("المنيا", False)],
            2,
        ),
    ],
)
def test_view_filter_simple_keyword_search(
    admin_client: Client,
    urls: dict[str, str],
    querystring: str,
    data: list[tuple[str, bool]],
    page_number: int,
):
    url: str = urls["index"] + querystring
    response = admin_client.get(url)

    assert response.status_code == 200

    for item in data:
        name, exists = item
        if exists:
            assert name in response.content.decode()
        else:
            assert name not in response.content.decode()

    assert response.context["page"].paginator.count == page_number
