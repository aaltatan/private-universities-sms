from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from apps.core.models import User

from .. import models


class TestGovernorateFilter(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )

        models.Governorate.objects.create(
            name="Hamah",
            description="google",
        )
        models.Governorate.objects.create(
            name="Halab",
            description="go language",
        )
        models.Governorate.objects.create(
            name="Homs",
            description="meta",
        )
        models.Governorate.objects.create(
            name="Damascus",
            description="meta",
        )

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.headers = {
            "HX-Request": "true",
        }

    def test_export_response_xlsx(self):
        url = reverse("governorates:index") + "?export=true&extension=xlsx"

        response = self.client.get(url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("HX-Redirect"))

        url += "&redirected=true"

        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"],
            "application/vnd.ms-excel",
        )

        str_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"Governorates-{str_now}.xlsx"

        self.assertEqual(
            response.headers["Content-Disposition"],
            f'attachment; filename="{filename}"',
        )

    def test_export_response_csv(self):
        url = reverse("governorates:index") + "?export=true&extension=csv"

        response = self.client.get(url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("HX-Redirect"))

        url += "&redirected=true"

        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"],
            "text/csv",
        )

        str_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"Governorates-{str_now}.csv"

        self.assertEqual(
            response.headers["Content-Disposition"],
            f'attachment; filename="{filename}"',
        )

    def test_export_response_json(self):
        url = reverse("governorates:index") + "?export=true&extension=json"

        response = self.client.get(url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("HX-Redirect"))

        url += "&redirected=true"

        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"],
            "application/json",
        )

        str_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"Governorates-{str_now}.json"

        self.assertEqual(
            response.headers["Content-Disposition"],
            f'attachment; filename="{filename}"',
        )

        self.assertEqual(
            response.json(),
            [
                {
                    "id": "1",
                    "Name": "Hamah",
                    "Description": "google",
                    "Slug": "hamah",
                },
                {
                    "id": "2",
                    "Name": "Halab",
                    "Description": "go language",
                    "Slug": "halab",
                },
                {
                    "id": "3",
                    "Name": "Homs",
                    "Description": "meta",
                    "Slug": "homs",
                },
                {
                    "id": "4",
                    "Name": "Damascus",
                    "Description": "meta",
                    "Slug": "damascus",
                },
            ],
        )
