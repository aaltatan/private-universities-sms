from collections import namedtuple

import pytest


Page = namedtuple("Query", ["q", "count", "next", "prev"])


@pytest.fixture(
    scope="package",
    params=[
        Page(q="", count=10, next="?page=2", prev=None),
        Page(q="?page=fsfs", count=10, next="?page=2", prev=None),
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
            "?kind=administrative",
            50,
            "name",
            ("Group 001", "Group 003"),
            ("Group 002", "Group 004"),
        ),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("?ordering=id", (1, 2, 10)),
    ],
)
def order_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("", "academic", ""),
        ("x", "academic", "x"),
        ("xx", "academic", "xx"),
        ("xxx", "academic", "xxx"),
        ("xxxx", "academicx", "xxx"),
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
            {"name": "Ha", "kind": "academic", "description": "google"},
            ["the field must be at least 4 characters long."],
        ),
        (
            {"name": "", "kind": "academic", "description": ""},
            ["This field is required."],
        ),
        (
            {"name": "a" * 265, "kind": "academic", "description": ""},
            ["Ensure this value has at most 255 characters (it has 265)."],
        ),
        (
            {"name": "Group 003", "kind": "academic", "description": "google"},
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
            {"name": "Ha", "kind": "academic", "description": "google"},
            {"name": ["Ensure this field has at least 4 characters."]},
        ),
        (
            {"name": "", "kind": "academic", "description": ""},
            {"name": ["This field may not be blank."]},
        ),
        (
            {"name": "a" * 265, "kind": "academic", "description": ""},
            {"name": ["Ensure this field has no more than 255 characters."]},
        ),
        (
            {"name": "Group 002", "kind": "academic", "description": "google"},
            {"name": ["Group with this name already exists."]},
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
