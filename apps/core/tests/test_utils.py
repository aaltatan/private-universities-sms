from django.test import SimpleTestCase

from ..utils import Perm, increase_slug_by_one


class TestPerm(SimpleTestCase):

    def test_increase_slug_by_one(self):
        slugs = [
            ('text', 'text1'),
            ('text-2', 'text-3'),
            ('text0', 'text1'),
            ('', ''),
            ('dAFSFAeqwd', 'dafsfaeqwd1'),
            ('2', '3'),
            ('a', 'a1')
        ]
        for slug, expected_slug in slugs:
            self.assertEqual(
                increase_slug_by_one(slug),
                expected_slug,
            )

    def test_perm_dataclass(self):
        perm = Perm("governorates")
        self.assertEqual(
            perm.string,
            "governorates.view_governorate",
        )

        permissions = ["add", "change", "delete", "export", "view"]

        for permission in permissions:
            perm = Perm("governorates", permission)
            self.assertEqual(
                perm.string,
                f"governorates.{permission}_governorate",
            )

        for permission in permissions:
            perm = Perm("cost_centers", permission)
            self.assertEqual(
                perm.string,
                f"cost_centers.{permission}_costcenter",
            )

        for permission in permissions:
            perm = Perm("faculties", permission)
            self.assertEqual(
                perm.string,
                f"faculties.{permission}_faculty",
            )

        for permission in permissions:
            perm = Perm(
                "education_transactions",
                permission,
                object_name="education_transaction",
            )
            self.assertEqual(
                perm.string,
                f"education_transactions.{permission}_educationtransaction",
            )
