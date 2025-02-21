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
            [f"School 00{i}" for i in range(1, 10, 2)],
            [f"School 00{i}" for i in range(2, 10, 2)],
        ),
        (
            "?is_virtual=True",
            50,
            "name",
            [f"School 00{i}" for i in range(1, 10, 2)],
            [f"School 00{i}" for i in range(2, 10, 2)],
        ),
        (
            "?q=School 00",
            10,
            "name",
            [f"School 00{i}" for i in range(1, 10)] + ["School 100"],
            [f"School 0{i}" for i in range(10, 100)],
        ),
        (
            "?q=id > 90",
            10,
            "name",
            [f"School 0{i}" for i in range(91, 100)],
            [f"School 0{i}" for i in range(10, 90)],
        ),
        (
            "?nationality=Nationality 002&nationality=Nationality 003&ordering=id&per_page=20",
            20,
            "name",
            [f"School 0{idx}" for idx in range(11, 30)],
            [f"School 00{idx}" for idx in range(1, 10)],
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
        (
            "x",
            1,
            False,
            False,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "xx",
            1,
            False,
            False,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "xxx",
            1,
            False,
            False,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "dasdasd",
            1,
            "dasd",
            False,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "dasdasd",
            1,
            True,
            "dasdasd",
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "dasdasd",
            1,
            True,
            "dasdasd",
            "a.altatan",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "dasdasd",
            1,
            True,
            "dasdasd",
            "a.altatan@gmail.com",
            "httcom",
            "1234567890",
            "dasdasd",
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
        (
            {
                "name": "Ha",
                "nationality": "Nationality 001",
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            ["the field must be at least 4 characters long."],
        ),
        (
            {
                "name": "",
                "nationality": "Nationality 001",
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            ["This field is required."],
        ),
        (
            {
                "name": "a" * 265,
                "nationality": "Nationality 001",
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
                "name": "School 002",
                "nationality": "Nationality 001",
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            ["School with this Name already exists."],
        ),
        (
            {
                "name": "School 002",
                "nationality": "Nationality 001",
                "is_virtual": False,
                "description": "google",
            },
            [
                "School with this Name already exists.",
                "This field is required.",
            ],
        ),
        (
            {
                "name": "School 002",
                "nationality": "Nationality 001",
                "is_governmental": True,
                "description": "google",
            },
            [
                "School with this Name already exists.",
                "This field is required.",
            ],
        ),
        (
            {
                "name": "Schoolxx 002",
                "nationality": "xxx",
                "is_governmental": True,
                "is_virtual": True,
                "description": "google",
            },
            ["this choice is not valid"],
        ),
        (
            {
                "name": "Schoolxx 002",
                "nationality": "Nationality 001",
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
                "nationality": "Nationality 001",
                "is_governmental": False,
                "is_virtual": "dasd",
                "description": "google",
            },
            [
                "Select a valid choice. dasd is not one of the available choices.",
            ],
        ),
        (
            {
                "name": "Schoolxx 002",
                "nationality": "Nationality 001",
                "is_governmental": False,
                "is_virtual": False,
                "description": "google",
                "email": "a.altatan"
            },
            [
                "Enter a valid email address.",
            ],
        ),
        (
            {
                "name": "Schoolxx 002",
                "nationality": "Nationality 001",
                "is_governmental": False,
                "is_virtual": False,
                "description": "google",
                "email": "a.altatan@gmail.com",
                "website": "dasdasd",
            },
            [
                "Enter a valid URL.",
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
                "nationality": 1,
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            {"name": ["Ensure this field has at least 4 characters."]},
        ),
        (
            {
                "name": "",
                "nationality": 1,
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            {"name": ["This field may not be blank."]},
        ),
        (
            {
                "name": "a" * 265,
                "nationality": 1,
                "is_governmental": True,
                "is_virtual": False,
                "description": "",
            },
            {"name": ["Ensure this field has no more than 255 characters."]},
        ),
        (
            {
                "name": "School 002",
                "nationality": 1,
                "is_governmental": True,
                "is_virtual": False,
                "description": "google",
            },
            {"name": ["school with this name already exists."]},
        ),
        (
            {
                "name": "School 002",
                "nationality": 1,
                "is_governmental": "sads",
                "is_virtual": "dasdasd",
                "description": "google",
            },
            {
                "name": ["school with this name already exists."],
                "is_governmental": ["Must be a valid boolean."],
                "is_virtual": ["Must be a valid boolean."],
            },
        ),
        (
            {
                "name": "School 002xx",
                "nationality": 1141412,
            },
            {
                "nationality": ['Invalid pk "1141412" - object does not exist.'],
            },
        ),
        (
            {
                "name": "School 002xx",
                "nationality": 1,
                "email": "dasdasd"
            },
            {
                "email": ['Enter a valid email address.'],
            },
        ),
        (
            {
                "name": "School 002xx",
                "nationality": 1,
                "email": "a.altatan@gmail.com",
                "website": "dasdasd"
            },
            {
                "website": ['Enter a valid URL.'],
            },
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
