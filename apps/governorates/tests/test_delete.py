from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.contrib import messages

from django.urls import reverse
from selectolax.parser import HTMLParser

from apps.core.models import User

from ..models import Governorate


class GovernorateCreateTest(TestCase):
    model = Governorate

    @classmethod
    def setUpTestData(cls):
        user_with_view_perm_only = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="user",
        )
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )
        view_perm = Permission.objects.get(
            codename="view_governorate",
        )
        user_with_view_perm_only.user_permissions.add(view_perm)

        for idx in range(1, 5):
            Governorate.objects.create(
                name=f"Governorate {idx}",
                description=f"Description {idx}",
            )

    def setUp(self):
        self.client.login(username="admin", password="admin")

        app_label = self.model._meta.app_label
        self.index_url = reverse(f"{app_label}:index")

    def test_delete_btn_appearance_if_user_has_delete_perm(
        self,
    ) -> None:
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        btn = parser.css_first("a[aria-label='delete object']")
        self.assertIsNotNone(btn)

    def test_delete_btn_appearance_if_user_has_no_delete_perm(
        self,
    ) -> None:
        self.client.logout()
        self.client.login(username="user", password="user")

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        btn = parser.css_first("a[aria-label='delete object']")

        self.assertIsNone(btn)

        obj = self.model.objects.first()

        response = self.client.get(obj.get_delete_url())

        self.assertEqual(response.status_code, 403)