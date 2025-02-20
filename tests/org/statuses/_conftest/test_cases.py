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
            "?is_payable=True",
            50,
            "name",
            [f"Status 00{idx}" for idx in range(1, 10, 2)],
            [f"Status 00{idx}" for idx in range(0, 10, 2)],
        ),
        (
            "?name=099 Status",
            1,
            "name",
            ("Status 099",),
            ("Status 003", "Status 050"),
        ),
        (
            "?q=id > 2&ordering=id",
            98,
            "name",
            ("Status 003", "Status 004"),
            ("Status 001", "Status 002"),
        ),
        (
            '?q=name startswith "Status 00"',
            9,
            "name",
            [f"Status 00{idx}" for idx in range(1, 10)],
            ("Status 100", "Status 099"),
        ),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("?ordering=id", (1, 2, 10)),
        ("?ordering=-id", (100, 99, 91)),
        ("?ordering=is_payable", (2, 4, 20)),
        ("?ordering=-is_payable", (1, 3, 19)),
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
            {"name": "Ha", "is_payable": True, "description": "google"},
            ["the field must be at least 4 characters long."],
        ),
        (
            {"name": "", "is_payable": True, "description": ""},
            ["This field is required."],
        ),
        (
            {"name": "a" * 265, "is_payable": True, "description": ""},
            ["Ensure this value has at most 255 characters (it has 265)."],
        ),
        (
            {
                "name": "Status 100",
                "is_payable": True,
                "description": "google",
            },
            ["Status with this Name already exists."],
        ),
        (
            {
                "name": "Status 100",
                "is_payable": "sss",
                "description": "google",
            },
            [
                "Status with this Name already exists.",
                "Select a valid choice. sss is not one of the available choices.",
            ],
        ),
        (
            {
                "name": "Status 1312",
                "is_payable": 4,
                "description": "google",
            },
            [
                "Select a valid choice. 4 is not one of the available choices.",
            ],
        ),
        (
            {
                "name": "Na",
                "is_payable": 4,
                "description": "google",
            },
            [
                "the field must be at least 4 characters long.",
                "Select a valid choice. 4 is not one of the available choices.",
            ],
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
            {"name": "Status 001", "description": "google"},
            {"name": ["status with this name already exists."]},
        ),
        (
            {"name": "Status 3131", "is_payable": "3123", "description": "google"},
            {"is_payable": ["Must be a valid boolean."]},
        ),
        (
            {"name": "Status 3131", "is_payable": 3123, "description": "google"},
            {"is_payable": ["Must be a valid boolean."]},
        ),
        (
            {"name": "Na", "is_payable": 3123, "description": "google"},
            {
                "name": ["Ensure this field has at least 4 characters."],
                "is_payable": ["Must be a valid boolean."],
            },
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
