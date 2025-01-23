from apps.core.utils import Perm, increase_slug_by_one


def test_increase_slug_by_one():
    slugs = [
        ("text", "text1"),
        ("text-2", "text-3"),
        ("text0", "text1"),
        ("", ""),
        ("dAFSFAeqwd", "dafsfaeqwd1"),
        ("2", "3"),
        ("a", "a1"),
    ]
    for slug, expected_slug in slugs:
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
