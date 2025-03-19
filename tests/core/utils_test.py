from datetime import datetime

import pytest

from apps.core.schemas import Perm
from apps.core.utils import (
    dict_to_css,
    get_differences,
    increase_slug_by_one,
    calculate_age_in_years,
)


@pytest.mark.parametrize(
    "birth_date, expected_age",
    [
        (datetime(2000, 1, 1), 25),
        (datetime(2007, 1, 1), 18),
        (datetime(2007, 2, 1), 18),
        (datetime(2007, 3, 17), 18),
        (datetime(2007, 3, 18), 18),
        (datetime(2007, 3, 19), 18),
        (datetime(2007, 3, 20), 17),
        (datetime(2007, 3, 21), 17),
        (datetime(2007, 3, 22), 17),
    ],
)
def test_calculate_age_in_years(birth_date: datetime, expected_age: int):
    assert calculate_age_in_years(birth_date) == expected_age


@pytest.mark.parametrize(
    "from_, to, expected",
    [
        (
            {"a": "b", "c": "d"},
            {"a": "b", "c": "d"},
            {},
        ),
        (
            {"a": "b", "c": "d"},
            {"a": "b", "c": "e"},
            {"after": {"c": "e"}, "before": {"c": "d"}},
        ),
        (
            {"a": "b", "c": "d"},
            {"e": "f", "g": "h"},
            {
                "before": {"a": "b", "c": "d"},
                "after": {"e": "f", "g": "h"},
            },
        ),
        (
            {"a": "b", "b": "c", "c": "d"},
            {"a": "b", "c": "d", "d": "e"},
            {"after": {"d": "e"}, "before": {"b": "c"}},
        ),
    ],
)
def test_get_differences(from_: dict, to: dict, expected: dict):
    assert get_differences(from_, to) == expected


@pytest.mark.parametrize(
    "dict_styles, expected_styles",
    [
        (
            {"a": "b", "c": "d"},
            "a: b; c: d;",
        ),
        (
            {"a": "b", "c": "d", "e": "f"},
            "a: b; c: d; e: f;",
        ),
        (
            {"a": "b", "c": "d", "e": "f", "g": "h"},
            "a: b; c: d; e: f; g: h;",
        ),
    ],
)
def test_dict_to_css(dict_styles: dict[str, str], expected_styles: str):
    assert dict_to_css(dict_styles) == expected_styles


@pytest.mark.parametrize(
    "slug, expected_slug",
    [
        ("text", "text1"),
        ("text-2", "text-3"),
        ("text0", "text1"),
        ("", ""),
        ("dAFSFAeqwd", "dafsfaeqwd1"),
        ("2", "3"),
        ("a", "a1"),
    ],
)
def test_increase_slug_by_one(slug: str, expected_slug: str):
    assert increase_slug_by_one(slug) == expected_slug


def test_perm_dataclass():
    perm = Perm("governorates")
    assert perm.string == "governorates.view_governorate"

    permissions = ["add", "change", "delete", "export", "view"]

    for permission in permissions:
        perm = Perm("governorates", permission)
        assert perm.string == f"governorates.{permission}_governorate"

    for permission in permissions:
        perm = Perm("cost_centers", permission)
        assert perm.string == f"cost_centers.{permission}_costcenter"

    for permission in permissions:
        perm = Perm("faculties", permission)
        assert perm.string == f"faculties.{permission}_faculty"

    for permission in permissions:
        perm = Perm(
            "education_transactions",
            permission,
            object_name="education_transaction",
        )
        assert (
            perm.string == f"education_transactions.{permission}_educationtransaction"
        )
