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
            "?is_governmental=True",
            50,
            "name",
            [f"SchoolKind 00{i}" for i in range(1, 10, 2)],
            [f"SchoolKind 00{i}" for i in range(2, 10, 2)],
        ),
        (
            "?is_virtual=True",
            50,
            "name",
            [f"SchoolKind 00{i}" for i in range(1, 10, 2)],
            [f"SchoolKind 00{i}" for i in range(2, 10, 2)],
        ),
        (
            "?q=SchoolKind 00",
            10,
            "name",
            [f"SchoolKind 00{i}" for i in range(1, 10)] + ["SchoolKind 100"],
            [f"SchoolKind 0{i}" for i in range(10, 100)],
        ),
        (
            "?q=id > 90",
            10,
            "name",
            [f"SchoolKind 0{i}" for i in range(91, 100)],
            [f"SchoolKind 0{i}" for i in range(10, 90)],
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
        ("x", False, False, "dasdasd"),
        ("xx", False, False, "dasdasd"),
        ("xxx", False, False, "dasdasd"),
        ("dasdasd", "dasd", False, "dasdasd"),
        ("dasdasd", True, "dasdasd", "dasdasd"),
        ("dasdasd", True, "dasdasd", "dasdasd"),
        ("dasdasd", True, "dasdasd", "dasdasd"),
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
            {
                "name": "Ha",
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            ["the field must be at least 4 characters long."],
        ),
        (
            {
                "name": "",
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            ["This field is required."],
        ),
        (
            {
                "name": "a" * 265,
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            [
                "Ensure this value has at most 255 characters (it has 265).",
            ],
        ),
        (
            {
                "name": "SchoolKind 002",
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            ["School Kind with this Name already exists."],
        ),
        (
            {
                "name": "SchoolKind 002",
                "is_virtual": False,
                "description": "google",
            },
            [
                "School Kind with this Name already exists.",
                "This field is required.",
            ],
        ),
        (
            {
                "name": "SchoolKind 002",
                "is_governmental": True,
                "description": "google",
            },
            [
                "School Kind with this Name already exists.",
                "This field is required.",
            ],
        ),
        (
            {
                "name": "Schoolxx 002",
                "is_governmental": "dasd",
                "is_virtual": True,
                "description": "google",
            },
            [
                "Select a valid choice. dasd is not one of the available choices.",
            ],
        ),
        (
            {
                "name": "Schoolxx 002",
                "is_governmental": False,
                "is_virtual": "dasd",
                "description": "google",
            },
            [
                "Select a valid choice. dasd is not one of the available choices.",
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
            {
                "name": "Ha",
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            {"name": ["Ensure this field has at least 4 characters."]},
        ),
        (
            {
                "name": "",
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            {"name": ["This field may not be blank."]},
        ),
        (
            {
                "name": "a" * 265,
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            {"name": ["Ensure this field has no more than 255 characters."]},
        ),
        (
            {
                "name": "SchoolKind 002",
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            {"name": ["School Kind with this name already exists."]},
        ),
        (
            {
                "name": "SchoolKind 002",
                "is_governmental": "sads",
                "is_virtual": "dasdasd",
                "description": "google",
            },
            {
                "name": ["School Kind with this name already exists."],
                "is_governmental": ["Must be a valid boolean."],
                "is_virtual": ["Must be a valid boolean."],
            },
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
