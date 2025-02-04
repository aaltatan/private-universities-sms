import pytest


@pytest.fixture(
    scope="package",
    params=[
        ("", 10, "?page=2", None),
        ("?page=2", 10, "?page=3", ""),
        ("?page=31", 4, None, "?page=30"),
    ]
    + [(f"?page={i}", 10, f"?page={i+1}", f"?page={i-1}") for i in range(3, 30)],
)
def api_pagination_test_cases(request: pytest.FixtureRequest):
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
            "?q=حم",
            2,
            [["حماه", True], ["حمص", True], ["ادلب", False], ["المنيا", False]],
        ),
        (
            "?q=meta",
            2,
            [["حماه", False], ["حمص", True], ["ادلب", True], ["المنيا", False]],
        ),
        (
            "?q=mena+language",
            1,
            [["حماه", False], ["حمص", False], ["ادلب", False], ["المنيا", True]],
        ),
        (
            "?q=id > 2&ordering=-name",
            302,
            [["حماه", False], ["حمص", False], ["ادلب", True], ["المنيا", True]],
        ),
        (
            '?q=id > 2 and name ~ "ل"&ordering=-name',
            2,
            [["حماه", False], ["حمص", False], ["ادلب", True], ["المنيا", True]],
        ),
        (
            "?q=id > 2 and name ~ 'ل'",  # using ' instead of "
            0,
            [["حماه", False], ["حمص", False], ["ادلب", False], ["المنيا", False]],
        ),
        (
            "?q=id in (1, 3)",
            2,
            [["حماه", True], ["حمص", False], ["ادلب", True], ["المنيا", False]],
        ),
    ],
)
def filters_test_cases(request: pytest.FixtureRequest):
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
        ("?page=2", 10, 2),
        ("?page=dasd", 10, 1),
        ("?page=21&per_page=50", 4, 7),
        ("?page=12&per_page=100", 4, 4),
        ("?page=dasd&per_page=all", 304, 1),
    ],
)
def pagination_test_cases(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(
    scope="package",
    params=[
        (
            "?ordering=Id",
            [1, 2, 10],
            ["محافظة حماه", "محافظة حمص", "City 006"],
            ["goo", "meta", "006"],
        ),
        (
            "?page=21&ordering=Id",
            [201, 202, 210],
            ["City 197", "City 198", "City 206"],
            ["197", "198", "206"],
        ),
        (
            "?page=1&ordering=-Id",
            [304, 303, 295],
            ["City 300", "City 299", "City 291"],
            ["300", "299", "291"],
        ),
        (
            "?ordering=Name",
            [5, 6, 14],
            ["City 001", "City 002", "City 010"],
            ["001", "002", "010"],
        ),
        (
            "?ordering=Description",
            [5, 6, 14],
            ["City 001", "City 002", "City 010"],
            ["001", "002", "010"],
        ),
        (
            "?page=21&ordering=Name",
            [205, 206, 214],
            ["City 201", "City 202", "City 210"],
            ["201", "202", "210"],
        ),
    ],
)
def order_test_cases(request: pytest.FixtureRequest):
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
