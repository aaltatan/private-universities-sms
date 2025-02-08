from collections import namedtuple

import pytest


Page = namedtuple("Query", ["q", "count", "next", "prev"])


@pytest.fixture(
    scope="package",
    params=[
        Page(q="", count=10, next="?page=2", prev=None),
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
        ("?q=حم", 2, ("حماه", "حمص"), ("ادلب", "المنيا")),
        ("?q=meta", 2, ("ادلب", "حمص"), ("حماه", "المنيا")),
        ("?q=mena+language", 1, ("المنيا",), ("ادلب", "حمص", "حماه")),
        ("?q=id > 2&ordering=-name", 302, ("ادلب", "المنيا"), ("حمص", "حماه")),
        (
            '?q=id > 2 and name ~ "ل"&ordering=-name',
            2,
            ("ادلب", "المنيا"),
            ("حمص", "حماه"),
        ),
        ("?q=id > 2 and name ~ 'ل'", 0, (), ("حمص", "حماه", "ادلب", "المنيا")),
        ("?q=id in (1, 3)", 2, ("حماه", "ادلب"), ("حمص", "المنيا")),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            "?ordering=Id",
            [
                (1, "محافظة حماه", "goo"),
                (2, "محافظة حمص", "meta"),
                (10, "City 006", "006"),
            ],
        ),
        (
            "?page=21&ordering=Id",
            [
                (201, "City 197", "197"),
                (202, "City 198", "198"),
                (210, "City 206", "206"),
            ],
        ),
        (
            "?page=1&ordering=-Id",
            [
                (304, "City 300", "300"),
                (303, "City 299", "299"),
                (295, "City 291", "291"),
            ],
        ),
        (
            "?ordering=Name",
            [
                (5, "City 001", "001"),
                (6, "City 002", "002"),
                (14, "City 010", "010"),
            ],
        ),
        (
            "?ordering=Description",
            [
                (5, "City 001", "001"),
                (6, "City 002", "002"),
                (14, "City 010", "010"),
            ],
        ),
        (
            "?page=21&ordering=Name",
            [
                (205, "City 201", "201"),
                (206, "City 202", "202"),
                (214, "City 210", "210"),
            ],
        ),
    ],
)
def order_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("", 1, ""),
        ("x", 1, "x"),
        ("xx", 1, "xx"),
        ("xxx", 1, "xxx"),
        (
            "Valid City",
            13123,  # not valid governorate pk
            "some description",
        ),
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
            "the field must be at least 4 characters long",
            ["Ensure this field has at least 4 characters."],
        ),
        (
            {"name": "", "description": ""},
            "This field is required.",
            ["This field may not be blank."],
        ),
        (
            {"name": "a" * 265, "description": ""},
            "Ensure this value has at most 255 characters (it has 265).",
            ["Ensure this field has no more than 255 characters."],
        ),
        (
            {"name": "محافظة حماه", "description": "google"},
            "Governorate with this Name already exists.",
            ["governorate with this name already exists."],
        ),
    ],
)
def dirty_data_test_cases(request: pytest.FixtureRequest):
    return request.param
