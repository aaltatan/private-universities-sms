from collections import namedtuple

import pytest


Page = namedtuple("Query", ["q", "count", "next", "prev"])


@pytest.fixture(
    scope="package",
    params=[
        Page(q="", count=10, next="?page=2", prev=None),
        Page(q="?page=fasd", count=10, next="?page=2", prev=None),
        Page(q="?page=2", count=10, next="?page=3", prev="?page=1"),
        Page(q="?page=3", count=10, next="?page=4", prev="?page=2"),
        Page(q="?page=4", count=10, next="?page=5", prev="?page=3"),
        Page(
            q="?page=1&per_page=all", count=100, next="?page=2&per_page=all", prev=None
        ),
        Page(q="?page=2&per_page=all", count=1, next=None, prev="?page=1&per_page=all"),
        Page(q="?per_page=50", count=50, next="?page=2&per_page=50", prev=None),
        Page(
            q="?page=2&per_page=50",
            count=50,
            next="?page=3&per_page=50",
            prev="?page=1&per_page=50",
        ),
    ],
)
def pagination_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            "?q=حماه",
            11,
            "name",
            ("City 001", "City 002"),
            ("City 011", "City 012"),
        ),
        (
            "?name=001 City",
            1,
            "name",
            ("City 001",),
            ("City 011", "City 012", "City 002"),
        ),
        (
            "?q=id < 11",
            10,
            "name",
            ("City 001", "City 002"),
            ("City 011", "City 012"),
        ),
        (
            "?job_type=محافظة حمص&job_type=محافظة حماه&per_page=50",
            21,
            "name",
            ("City 011", "City 012"),
            ("City 090", "City 091"),
        ),
        (
            "?q=حماه محافظة",
            11,
            "name",
            ("City 001", "City 002"),
            ("City 011", "City 012"),
        ),
        (
            '?q=job_type.name ~ "حماه"',
            11,
            "name",
            ("City 001", "City 002"),
            ("City 011", "City 012"),
        ),
        (
            "?q=حم&per_page=20",
            21,
            "name",
            ("City 011", "City 012", "City 001", "City 002"),
            ("City 090", "City 091"),
        ),
        (
            "?q=حمص",
            10,
            "name",
            ("City 011", "City 012"),
            ("City 001", "City 002"),
        ),
        (
            "?q=2&per_page=20",
            19,
            "name",
            ("City 002", "City 012", "City 020", "City 021"),
            ("City 001", "City 011"),
        ),
        (
            '?q=name endswith "0"',
            10,
            "name",
            ("City 010", "City 020", "City 030", "City 040"),
            ("City 001", "City 011"),
        ),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        ("?ordering=Id", (1, 2, 10)),
        ("?ordering=Name", (1, 2, 10)),
        ("?ordering=Name&page=2", (11, 12, 20)),
        ("?page=21&ordering=Id", (101,)),
        ("?page=1&ordering=-Id", (101, 100, 92)),
        ("?ordering=Job+Type", (61, 62, 70)),
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
            13123,  # not valid job_type pk
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
        (
            {
                "name": "Ha",
                "job_type": "محافظة حمص",
                "description": "google",
            },
            ["the field must be at least 4 characters long."],
        ),
        (
            {
                "name": "",
                "job_type": "محافظة حمص",
                "description": "",
            },
            ["This field is required."],
        ),
        (
            {
                "name": "a" * 265,
                "job_type": "محافظة حمص",
                "description": "",
            },
            ["Ensure this value has at most 255 characters (it has 265)."],
        ),
        (
            {
                "name": "Hama City",
                "job_type": "محافظة حمص",
                "description": "google",
            },
            ["Job subtype with this Name already exists."],
        ),
        (
            {
                "name": "Hama City sdadsas",
                "job_type": "محافظة x",
                "description": "google",
            },
            ["this choice is not valid"],
        ),
        (
            {
                "name": "Ham",
                "job_type": "محافظة x",
                "description": "google",
            },
            [
                "the field must be at least 4 characters long.",
                "this choice is not valid",
            ],
        ),
        (
            {
                "name": "Ham",
                "job_type": "",
                "description": "google",
            },
            [
                "the field must be at least 4 characters long.",
                "This field is required.",
            ],
        ),
        (
            {
                "name": "",
                "job_type": "",
            },
            [
                "This field is required.",
            ]
            * 2,
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
                "job_type": 1,
                "description": "google",
            },
            {"name": ["Ensure this field has at least 4 characters."]},
        ),
        (
            {
                "name": "",
                "job_type": 2,
                "description": "",
            },
            {"name": ["This field may not be blank."]},
        ),
        (
            {
                "name": "a" * 265,
                "job_type": 3,
                "description": "",
            },
            {"name": ["Ensure this field has no more than 255 characters."]},
        ),
        (
            {
                "name": "Hama City",
                "job_type": 4,
                "description": "google",
            },
            {"name": ["job subtype with this name already exists."]},
        ),
        (
            {
                "name": "Hama City sss",
                "job_type_id": 4,
                "description": "google",
            },
            {"job_type": ["This field is required."]},
        ),
        (
            {
                "name": "Hama City sss",
                "job_type": "dasdas",
                "description": "google",
            },
            {"job_type": ["Incorrect type. Expected pk value, received str."]},
        ),
        (
            {
                "name": "Hama City sss",
                "job_type": 412312,
                "description": "google",
            },
            {"job_type": ['Invalid pk "412312" - object does not exist.']},
        ),
        (
            {
                "name": "Ham",
                "job_type": 412312,
                "description": "google",
            },
            {
                "name": ["Ensure this field has at least 4 characters."],
                "job_type": ['Invalid pk "412312" - object does not exist.'],
            },
        ),
        (
            {
                "name": "",
                "job_type": "412312",
                "description": "google",
            },
            {
                "name": ["This field may not be blank."],
                "job_type": ['Invalid pk "412312" - object does not exist.'],
            },
        ),
    ],
)
def dirty_data_api_test_cases(request: pytest.FixtureRequest):
    return request.param
