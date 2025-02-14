from collections import namedtuple

import pytest


Page = namedtuple("Query", ["q", "count", "next", "prev"])


@pytest.fixture(
    scope="package",
    params=[
        Page(q="", count=10, next="?page=2", prev=None),
        Page(q="?page=fsfs", count=10, next="?page=2", prev=None),
        Page(
            q="?page=1&per_page=all", count=100, next="?page=2&per_page=all", prev=None
        ),
        Page(q="?page=7&per_page=50", count=4, next=None, prev="?page=6&per_page=50"),
        Page(q="?page=31", count=4, next=None, prev="?page=30"),
        Page(q="?page=3", count=10, next="?page=4", prev="?page=2"),
        Page(q="?page=4", count=10, next="?page=5", prev="?page=3"),
        Page(q="?page=5", count=10, next="?page=6", prev="?page=4"),
        Page(q="?page=22", count=10, next="?page=23", prev="?page=21"),
    ],
)
def pagination_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            "?q=حم",
            2,
            "name",
            ("محافظة حماه", "محافظة حمص"),
            ("محافظة ادلب", "محافظة المنيا"),
        ),
        (
            "?name=حم محاف",
            2,
            "name",
            ("محافظة حماه", "محافظة حمص"),
            ("محافظة ادلب", "محافظة المنيا"),
        ),
        (
            "?q=meta",
            2,
            "name",
            ("محافظة ادلب", "محافظة حمص"),
            ("محافظة حماه", "محافظة المنيا"),
        ),
        (
            "?q=mena+language",
            1,
            "name",
            ("محافظة المنيا",),
            ("محافظة ادلب", "محافظة حمص", "محافظة حماه"),
        ),
        (
            "?q=id > 2&ordering=-name",
            302,
            "name",
            ("محافظة ادلب", "محافظة المنيا"),
            ("محافظة حمص", "محافظة حماه"),
        ),
        (
            '?q=id > 2 and name ~ "ل"&ordering=-name',
            2,
            "name",
            ("محافظة ادلب", "محافظة المنيا"),
            ("محافظة حمص", "محافظة حماه"),
        ),
        (
            "?q=id > 2 and name ~ 'ل'",
            0,
            "name",
            (),
            ("محافظة حمص", "محافظة حماه", "محافظة ادلب", "محافظة المنيا"),
        ),
        (
            "?q=id in (1, 3)",
            2,
            "name",
            ("محافظة حماه", "محافظة ادلب"),
            ("حمص", "محافظة المنيا"),
        ),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("?ordering=Id", (1, 2, 10)),
        ("?page=21&ordering=Id", (201, 202, 210)),
        ("?page=1&ordering=-Id", (304, 303, 295)),
        ("?ordering=Name", (5, 6, 14)),
        ("?ordering=Description", (5, 6, 14)),
        ("?page=21&ordering=Name", (205, 206, 214)),
    ],
)
def order_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("", ""),
        ("x", "x"),
        ("xx", "xx"),
        ("xxx", "xxx"),
    ],
)
def models_dirty_data_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("csv", "text/csv"),
        ("json", "application/json"),
        ("xlsx", "application/vnd.ms-excel"),
    ],
)
def export_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("حماه", "محافظة حماه", "محافظة حماه", "محافظة-حماه"),
        ("حمص", "محافظة حمص", "محافظة حمص", "محافظة-حمص"),
        ("ادلب", "محافظة ادلب", "محافظة ادلب", "محافظة-ادلب"),
        ("المنيا", "محافظة المنيا", "محافظة المنيا", "محافظة-المنيا"),
    ],
)
def models_data_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            {"name": "Ha", "description": "google"},
            ["the field must be at least 4 characters long."],
        ),
        (
            {"name": "", "description": ""},
            ["This field is required."],
        ),
        (
            {"name": "a" * 265, "description": ""},
            ["Ensure this value has at most 255 characters (it has 265)."],
        ),
        (
            {"name": "محافظة حماه", "description": "google"},
            ["Group with this Name already exists."],
        ),
    ],
)
def dirty_data_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            {"name": "Ha", "description": "google"},
            {"name": ["Ensure this field has at least 4 characters."]},
        ),
        (
            {"name": "", "description": ""},
            {"name": ["This field may not be blank."]},
        ),
        (
            {"name": "a" * 265, "description": ""},
            {"name": ["Ensure this field has no more than 255 characters."]},
        ),
        (
            {"name": "محافظة حماه", "description": "google"},
            {"name": ["group with this name already exists."]},
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
