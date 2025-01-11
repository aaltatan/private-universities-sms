import json
import re

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
            password="user",
        )
        User.objects.create_superuser(
            username="admin",
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
        self.delete_modal_template = "components/blocks/modals/delete.html"

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

    def test_get_delete_modal_without_using_htmx(self) -> None:
        obj = self.model.objects.first()

        response = self.client.get(obj.get_delete_url())

        self.assertEqual(response.status_code, 404)

    def test_get_delete_modal_with_using_htmx(self) -> None:
        obj = self.model.objects.first()

        headers = {"Hx-Request": "true"}

        response = self.client.get(
            obj.get_delete_url(),
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            self.delete_modal_template,
        )

        parser = HTMLParser(response.content)
        modal_body = parser.css_first(
            "#modal-container p",
        ).text(strip=True)

        modal_body = re.sub(r"\s+", " ", modal_body)

        self.assertEqual(
            modal_body,
            "are you sure you want to delete Governorate 1 ?",
        )

    def test_delete_object(self) -> None:
        obj = self.model.objects.first()

        headers = {"Hx-Request": "true"}

        response = self.client.post(obj.get_delete_url(), headers=headers)

        self.assertEqual(response.status_code, 204)
        location = json.loads(
            response.headers.get("Hx-Location", {}),
        )
        location_path = location.get("path", "")
        self.assertEqual(location_path, self.index_url)

        self.assertEqual(
            response.headers.get("Hx-Trigger"),
            "messages",
        )

        messages_list = list(
            get_messages(response.wsgi_request),
        )
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 3)
