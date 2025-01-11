from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from selectolax.parser import HTMLParser

from apps.core.models import User

from .. import models


class GovernoratesViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )

        models.Governorate.objects.create(
            name="Governorate 1",
            description="google",
        )
        models.Governorate.objects.create(
            name="Governorate 2",
            description="goo language",
        )
        models.Governorate.objects.create(
            name="Governorate 3",
            description="meta",
        )

        cls.index_url = reverse("governorates:index")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_view_index_file(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/governorates/index.html")

    def test_view_has_all_html_elements_which_need_permissions(self):
        response = self.client.get(self.index_url)
        parser = HTMLParser(response.content)

        add_new_btn = parser.css_first(
            "[aria-label='create new object']",
        )
        add_new_btn_exists = add_new_btn is not None

        export_btn = parser.css_first(
            "a[aria-label^='export table']",
        )
        export_btn_exists = export_btn is not None

        row_delete_btn = parser.css_first(
            "a[aria-label='delete object']",
        )
        row_delete_btn_exists = row_delete_btn is not None

        row_edit_btn = parser.css_first(
            "a[aria-label='edit object']",
        )
        row_edit_btn_exists = row_edit_btn is not None

        row_delete_all_btn = parser.css_first(
            "input[aria-label='delete all objects']",
        )
        row_delete_all_btn_exists = row_delete_all_btn is not None

        self.assertTrue(add_new_btn_exists)
        self.assertTrue(export_btn_exists)
        self.assertTrue(row_delete_btn_exists)
        self.assertTrue(row_edit_btn_exists)
        self.assertTrue(row_delete_all_btn_exists)

    def test_view_contains_objects(self):
        response = self.client.get(self.index_url)

        self.assertContains(response, "Governorate 1")
        self.assertContains(response, "Governorate 2")
        self.assertContains(response, "Governorate 3")

        self.assertContains(response, "google")
        self.assertContains(response, "goo language")
        self.assertContains(response, "meta")


class TestViewsPermission(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Governorate.objects.create(
            name="Governorate 1",
            description="google",
        )
        models.Governorate.objects.create(
            name="Governorate 2",
            description="goo language",
        )
        models.Governorate.objects.create(
            name="Governorate 3",
            description="meta",
        )

        strings: tuple[str] = (
            "user_without_view",
            "user_with_view",
            "user_with_view_add",
            "user_with_view_change",
            "user_with_view_delete",
            "user_with_view_export",
            "user_with_view_add_change",
        )
        users: dict[str, User] = {}
        for user in strings:
            user_with_view = User.objects.create_user(
                username=user,
                password=user,
            )
            users[user] = user_with_view

        view_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="view_governorate",
        )
        delete_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="delete_governorate",
        )
        add_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="add_governorate",
        )
        change_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="change_governorate",
        )
        export_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="export_governorate",
        )

        users["user_with_view"].user_permissions.add(view_perm)
        users["user_with_view_add"].user_permissions.add(
            add_perm,
            view_perm,
        )
        users["user_with_view_change"].user_permissions.add(
            change_perm,
            view_perm,
        )
        users["user_with_view_delete"].user_permissions.add(
            delete_perm,
            view_perm,
        )
        users["user_with_view_export"].user_permissions.add(
            export_perm,
            view_perm,
        )
        users["user_with_view_add_change"].user_permissions.add(
            add_perm,
            change_perm,
            view_perm,
        )

        cls.index_url = reverse("governorates:index")

    def _get_buttons(self, parser: HTMLParser) -> dict[str, bool]:
        add_btn = parser.css_first(
            "[aria-label='create new object']",
        )
        delete_btn = parser.css_first(
            "a[aria-label='delete object']",
        )
        delete_all_btn = parser.css_first(
            "input[aria-label='delete all objects']",
        )
        edit_btn = parser.css_first(
            "a[aria-label='edit object']",
        )
        export_btn = parser.css_first(
            "a[aria-label^='export table']",
        )

        return {
            "add_btn_exists": add_btn is not None,
            "delete_btn_exists": delete_btn is not None,
            "delete_all_btn_exists": delete_all_btn is not None,
            "edit_btn_exists": edit_btn is not None,
            "export_btn_exists": export_btn is not None,
        }

    def test_view_user_has_no_permissions(self):
        self.client.login(
            username="user_without_view",
            password="user_without_view",
        )

        self.client.login(username="user", password="user")

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 403)

    def test_view_user_has_view_permissions(self):
        self.client.login(username="user_with_view", password="user_with_view")

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        buttons = self._get_buttons(parser)

        self.assertFalse(buttons["add_btn_exists"])
        self.assertFalse(buttons["delete_btn_exists"])
        self.assertFalse(buttons["delete_all_btn_exists"])
        self.assertFalse(buttons["edit_btn_exists"])
        self.assertFalse(buttons["export_btn_exists"])

    def test_view_user_has_view_permissions_add(self):
        self.client.login(username="user_with_view_add", password="user_with_view_add")
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        parser = HTMLParser(response.content)
        buttons = self._get_buttons(parser)
        self.assertTrue(buttons["add_btn_exists"])
        self.assertFalse(buttons["delete_btn_exists"])
        self.assertFalse(buttons["delete_all_btn_exists"])
        self.assertFalse(buttons["edit_btn_exists"])
        self.assertFalse(buttons["export_btn_exists"])

    def test_view_user_has_view_permissions_change(self):
        self.client.login(
            username="user_with_view_change", password="user_with_view_change"
        )
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        parser = HTMLParser(response.content)
        buttons = self._get_buttons(parser)
        self.assertFalse(buttons["add_btn_exists"])
        self.assertFalse(buttons["delete_btn_exists"])
        self.assertFalse(buttons["delete_all_btn_exists"])
        self.assertTrue(buttons["edit_btn_exists"])
        self.assertFalse(buttons["export_btn_exists"])

    def test_view_user_has_view_permissions_delete(self):
        self.client.login(
            username="user_with_view_delete", password="user_with_view_delete"
        )
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        parser = HTMLParser(response.content)
        buttons = self._get_buttons(parser)
        self.assertFalse(buttons["add_btn_exists"])
        self.assertTrue(buttons["delete_btn_exists"])
        self.assertTrue(buttons["delete_all_btn_exists"])
        self.assertFalse(buttons["edit_btn_exists"])
        self.assertFalse(buttons["export_btn_exists"])

    def test_view_user_has_view_permissions_export(self):
        self.client.login(
            username="user_with_view_export", password="user_with_view_export"
        )
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        parser = HTMLParser(response.content)
        buttons = self._get_buttons(parser)
        self.assertFalse(buttons["add_btn_exists"])
        self.assertFalse(buttons["delete_btn_exists"])
        self.assertFalse(buttons["delete_all_btn_exists"])
        self.assertFalse(buttons["edit_btn_exists"])
        self.assertTrue(buttons["export_btn_exists"])

    def test_view_user_has_view_permissions_add_change(self):
        self.client.login(
            username="user_with_view_add_change", password="user_with_view_add_change"
        )
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        parser = HTMLParser(response.content)
        buttons = self._get_buttons(parser)
        self.assertTrue(buttons["add_btn_exists"])
        self.assertFalse(buttons["delete_btn_exists"])
        self.assertFalse(buttons["delete_all_btn_exists"])
        self.assertTrue(buttons["edit_btn_exists"])
        self.assertFalse(buttons["export_btn_exists"])
