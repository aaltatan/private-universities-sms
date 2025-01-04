import re
import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib import messages

from selectolax.parser import HTMLParser

from apps.core.models import User

from .. import models


class TestGovernorateActions(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="user_without_perms",
            password="user_without_perms",
        )

        user_with_view_perm_only = User.objects.create_user(
            username="user_with_view_perm_only",
            email="user_with_view_perm_only@example.com",
            password="user_with_view_perm_only",
        )

        user_with_delete_perms = User.objects.create_user(
            username="user_with_delete_perms",
            email="user_with_delete_perms@example.com",
            password="user_with_delete_perms",
        )
        view_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="view_governorate",
        )
        delete_perm = Permission.objects.get(
            content_type__app_label="governorates",
            codename="delete_governorate",
        )
        user_with_delete_perms.user_permissions.add(
            view_perm,
            delete_perm,
        )
        user_with_view_perm_only.user_permissions.add(view_perm)

        object_list = [
            models.Governorate(name=f"City {idx}") 
            for idx in range(1, 301)
        ]

        models.Governorate.objects.bulk_create(object_list)

    def test_bulk_delete_modal_response(self):
        self.client.login(
            username="user_with_delete_perms",
            password="user_with_delete_perms",
        )

        url: str = reverse("governorates:index")

        data: dict = {
            "action-check": list(range(1, 51)),
            "kind": "modal",
            "name": "delete",
        }

        response = self.client.post(url, data)
        parser = HTMLParser(response.content)

        self.assertEqual(response.status_code, 200)

        modal_body = (
            parser.css_first("#modal-container > div > form > div:nth-child(2) p")
            .text(strip=True)
            .replace("\n", "")
            .strip()
        )

        modal_body = re.compile(r"\s{2,}").sub(" ", modal_body)

        self.assertEqual(
            modal_body,
            "are you sure you want to delete all 50 selected objects ?",
        )

    def test_bulk_delete_without_permissions(self):
        self.client.login(
            username="user_without_perms",
            password="user_without_perms",
        )

        url: str = reverse("governorates:index")

        data: dict = {
            "action-check": list(range(1, 51)),
            "kind": "action",
            "name": "delete",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_bulk_delete_with_permissions(self):
        self.client.login(
            username="user_with_delete_perms",
            password="user_with_delete_perms",
        )

        url: str = reverse("governorates:index")

        data: dict = {
            "action-check": list(range(1, 51)),
            "kind": "action",
            "name": "delete",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 204)
        self.assertIsNotNone(response.headers.get("Hx-Location"))

        hx_location = json.loads(
            response.headers.get("Hx-Location"),
        )

        self.assertEqual(hx_location["path"], url)

        messages_list = list(
            messages.get_messages(request=response.wsgi_request),
        )

        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(
            messages_list[0].message,
            "all (50) selected objects have been deleted successfully",
        )

        qs = models.Governorate.objects.all()
        self.assertEqual(qs.count(), 250)

    def test_bulk_action_not_found(self):
        self.client.login(
            username="user_with_delete_perms",
            password="user_with_delete_perms",
        )

        url: str = reverse("governorates:index")

        data: dict = {
            "action-check": list(range(1, 51)),
            "kind": "action",
            "name": "bulk_delete",  # name not in actions
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 500)

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 500)

    def test_bulk_delete_with_permissions_only_for_view(self):
        self.client.login(
            username="user_with_view_perm_only",
            password="user_with_view_perm_only",
        )

        url: str = reverse("governorates:index")

        data: dict = {
            "action-check": list(range(1, 51)),
            "kind": "action",
            "name": "delete",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
