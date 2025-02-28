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
            "?name=School 00",
            10,
            "name",
            [f"School 00{i}" for i in range(1, 10)] + ["School 100"],
            [f"School 0{i}" for i in range(10, 100)],
        ),
        (
            "?q=SchoolKind 001",
            10,
            "name",
            [f"School 00{i}" for i in range(1, 10)] + ["School 010"],
            [f"School 0{i}" for i in range(11, 100)],
        ),
        (
            "?kind=SchoolKind 001",
            10,
            "name",
            [f"School 00{i}" for i in range(1, 10)] + ["School 010"],
            [f"School 0{i}" for i in range(11, 100)],
        ),
        (
            "?kind=SchoolKind 001&kind=SchoolKind 002&per_page=20",
            20,
            "name",
            [f"School 00{i}" for i in range(1, 10)]
            + [f"School 0{i}" for i in range(10, 21)],
            [f"School 0{i}" for i in range(21, 100)],
        ),
        (
            "?nationality=Nationality 001",
            10,
            "name",
            [f"School 00{i}" for i in range(1, 10)] + ["School 010"],
            [f"School 0{i}" for i in range(11, 100)],
        ),
        (
            "?q=Nationality 001",
            10,
            "name",
            [f"School 00{i}" for i in range(1, 10)] + ["School 010"],
            [f"School 0{i}" for i in range(11, 100)],
        ),
        (
            "?nationality=Nationality 001&nationality=Nationality 002&per_page=20",
            20,
            "name",
            [f"School 00{i}" for i in range(1, 10)]
            + [f"School 0{i}" for i in range(10, 21)],
            [f"School 0{i}" for i in range(21, 100)],
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
            1,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "xx",
            1,
            1,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "xxx",
            1,
            1,
            "a.altatan@gmail.com",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "Al-Wataniya private university",
            1,
            1,
            "a.altatan",
            "https://www.google.com",
            "1234567890",
            "dasdasd",
        ),
        (
            "Al-Wataniya private university",
            1,
            1,
            "a.altatan@gmail.com",
            "dasdasdasd",
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
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            ["the field must be at least 4 characters long."],
        ),
        (
            {
                "name": "",
                "nationality": "Nationality 001",
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "",
            },
            ["This field is required."],
        ),
        (
            {
                "name": "a" * 265,
                "nationality": "Nationality 001",
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
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
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            ["School with this Name already exists."],
        ),
        (
            {
                "name": "School 002",
                "nationality": "xxxx",
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            [
                "School with this Name already exists.",
                "this choice is not valid",
            ],
        ),
        (
            {
                "name": "School 002",
                "nationality": "Nationality 001",
                "kind": "xxxx",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            [
                "School with this Name already exists.",
                "this choice is not valid",
            ],
        ),
        (
            {
                "name": "School 002",
                "nationality": "Nationality 001",
                "kind": "SchoolKind 001",
                "website": "dasdasd",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            [
                "School with this Name already exists.",
                "Enter a valid URL.",
            ],
        ),
        (
            {
                "name": "School 002",
                "nationality": "Nationality 001",
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan",
                "phone": "1234567890",
                "description": "google",
            },
            [
                "School with this Name already exists.",
                "Enter a valid email address.",
            ],
        ),
        (
            {
                "name": "School Google",
                "nationality": "Nationality 001",
                "kind": "SchoolKind 001",
                "website": "https://www.google.com",
                "email": "a.altatan-10@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            [
                "School with this Email already exists.",
            ],
        ),
        (
            {
                "name": "School Google",
                "nationality": "Nationality 001",
                "kind": "SchoolKind 001",
                "website": "https://google-10.com",
                "email": "a.altatan@hotmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            [
                "School with this Website already exists.",
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
                "kind": 1,
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {"name": ["Ensure this field has at least 4 characters."]},
        ),
        (
            {
                "name": "",
                "nationality": 1,
                "kind": 1,
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "",
            },
            {"name": ["This field may not be blank."]},
        ),
        (
            {
                "name": "a" * 265,
                "nationality": 1,
                "kind": 1,
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "",
            },
            {"name": ["Ensure this field has no more than 255 characters."]},
        ),
        (
            {
                "name": "School 002",
                "nationality": 1,
                "kind": 1,
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {"name": ["school with this name already exists."]},
        ),
        (
            {
                "name": "School xxxx",
                "nationality": "dasd",
                "kind": 1,
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {
                "nationality": [
                    "Incorrect type. Expected pk value, received str.",
                ],
            },
        ),
        (
            {
                "name": "School xxxx",
                "nationality": 1,
                "kind": "dasd",
                "website": "https://www.google.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {
                "kind": [
                    "Incorrect type. Expected pk value, received str.",
                ]
            },
        ),
        (
            {
                "name": "School xxxx",
                "nationality": 1,
                "kind": 1,
                "website": "com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {
                "website": [
                    "Enter a valid URL.",
                ]
            },
        ),
        (
            {
                "name": "School xxxx",
                "nationality": 1,
                "kind": 1,
                "website": "https://www.google.com",
                "email": "a.altatan-10@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {
                "email": [
                    "school with this email already exists.",
                ]
            },
        ),
        (
            {
                "name": "School xxxx",
                "nationality": 1,
                "kind": 1,
                "website": "https://google-10.com",
                "email": "a.altatan@gmail.com",
                "phone": "1234567890",
                "description": "google",
            },
            {
                "website": [
                    "school with this website already exists.",
                ]
            },
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
