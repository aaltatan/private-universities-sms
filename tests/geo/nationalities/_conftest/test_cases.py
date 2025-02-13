from collections import namedtuple

import pytest


Page = namedtuple("Query", ["q", "count", "next", "prev"])


@pytest.fixture(
    scope="package",
    params=[
        Page(q="", count=10, next="?page=2", prev=None),
        Page(q="?page=fsfs", count=10, next="?page=2", prev=None),
        Page(q="?page=1&per_page=all", count=100, next=None, prev=None),
        Page(q="?page=7&per_page=50", count=50, next=None, prev="?page=1&per_page=50"),
        Page(q="?page=3", count=10, next="?page=4", prev="?page=2"),
        Page(q="?page=4", count=10, next="?page=5", prev="?page=3"),
        Page(q="?page=5", count=10, next="?page=6", prev="?page=4"),
    ],
)
def pagination_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            "?is_local=True",
            1,
            "name",
            ("Nationality 099",),
            ("Nationality 003", "Nationality 050"),
        ),
        (
            "?q=id > 2",
            98,
            "name",
            ("Nationality 003", "Nationality 004"),
            ("Nationality 001", "Nationality 002"),
        ),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("?ordering=Id", (1, 2, 10)),
        ("?ordering=-Id", (100, 99, 91)),
        ("?ordering=-Locality", (99, 1, 9)),
    ],
)
def order_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("", True, ""),
        ("x", False, "x"),
        ("xx", False, "xx"),
        ("xxx", False, "xxx"),
        ("dasdasd", "dasd", "xfasdqwfqxx"),
        ("dasdasd", "", "xfasdqwfqxx"),
        ("dasdasd", 2, "xfasdqwfqxx"),
        ("dasdasd", None, "xfasdqwfqxx"),
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
        (
            {"name": "Ha", "is_local": True, "description": "google"},
            ["the field must be at least 4 characters long."],
        ),
        (
            {"name": "", "is_local": True, "description": ""},
            ["This field is required."],
        ),
        (
            {"name": "a" * 265, "is_local": True, "description": ""},
            ["Ensure this value has at most 255 characters (it has 265)."],
        ),
        (
            {"name": "Nationality 100", "is_local": True, "description": "google"},
            ["Nationality with this Name already exists."],
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
            {"name": "Nationality 001", "description": "google"},
            {"name": ["nationality with this name already exists."]},
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
