from django.test import TestCase
from django.urls import reverse

from selectolax.parser import HTMLParser

from apps.core.models import User

from .. import models


class TestGovernorateFilter(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username="admin",
            password="admin",
        )

        for idx in range(1, 301):
            description_order: str = str(abs(idx - 301)).rjust(3, "0")
            models.Governorate.objects.create(
                name=f"City {idx}", description=description_order
            )

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.index_url: str = reverse("governorates:index")
        self.object_name: str = "City"

    def test_view_filter_order_by_id_page_one(self):
        url: str = self.index_url + "?order_by=id"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["page"].object_list[0].id, 1)
        self.assertEqual(response.context["page"].object_list[1].id, 2)
        self.assertEqual(response.context["page"].object_list[-1].id, 10)

        self.assertEqual(
            response.context["page"].object_list[0].name,
            f"{self.object_name} 1",
        )
        self.assertEqual(
            response.context["page"].object_list[1].name,
            f"{self.object_name} 2",
        )
        self.assertEqual(
            response.context["page"].object_list[-1].name,
            f"{self.object_name} 10",
        )

    def test_view_filter_order_by_id_page_twenty_one(self):
        url: str = self.index_url + "?page=21&order_by=id"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["page"].object_list[0].id,
            201,
        )
        self.assertEqual(
            response.context["page"].object_list[1].id,
            202,
        )
        self.assertEqual(
            response.context["page"].object_list[-1].id,
            210,
        )

        self.assertEqual(
            response.context["page"].object_list[0].name,
            f"{self.object_name} 201",
        )
        self.assertEqual(
            response.context["page"].object_list[1].name,
            f"{self.object_name} 202",
        )
        self.assertEqual(
            response.context["page"].object_list[-1].name,
            f"{self.object_name} 210",
        )

    def test_view_filter_order_by_name_page_one(self):
        url: str = self.index_url + "?order_by=name"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["page"].object_list[0].name,
            f"{self.object_name} 1",
        )
        self.assertEqual(
            response.context["page"].object_list[1].name,
            f"{self.object_name} 2",
        )
        self.assertEqual(
            response.context["page"].object_list[-1].name,
            f"{self.object_name} 10",
        )

        self.assertEqual(
            response.context["page"].object_list[0].id,
            1,
        )
        self.assertEqual(
            response.context["page"].object_list[1].id,
            2,
        )
        self.assertEqual(
            response.context["page"].object_list[-1].id,
            10,
        )

    def test_view_filter_order_by_name_page_twenty_one(self):
        url: str = self.index_url + "?page=21&order_by=name"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["page"].object_list[0].name,
            f"{self.object_name} 201",
        )
        self.assertEqual(
            response.context["page"].object_list[1].name,
            f"{self.object_name} 202",
        )
        self.assertEqual(
            response.context["page"].object_list[-1].name,
            f"{self.object_name} 210",
        )

        self.assertEqual(
            response.context["page"].object_list[0].id,
            201,
        )
        self.assertEqual(
            response.context["page"].object_list[1].id,
            202,
        )
        self.assertEqual(
            response.context["page"].object_list[-1].id,
            210,
        )

    def test_view_filter_order_by_description_page_one(self):
        url: str = self.index_url + "?order_by=Description"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["page"].object_list[0].description,
            "001",
        )
        self.assertEqual(
            response.context["page"].object_list[1].description,
            "002",
        )
        self.assertEqual(
            response.context["page"].object_list[-1].description,
            "010",
        )

        self.assertEqual(
            response.context["page"].object_list[0].name,
            f"{self.object_name} 300",
        )
        self.assertEqual(
            response.context["page"].object_list[1].name,
            f"{self.object_name} 299",
        )
        self.assertEqual(
            response.context["page"].object_list[-1].name,
            f"{self.object_name} 291",
        )

    def test_view_pagination(self):
        url: str = self.index_url + "?page=2"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].number, 2)

        parser = HTMLParser(response.content)
        rows = parser.css("table tr:not(:first-child)")

        self.assertEqual(len(rows), 10)

    def test_pagination_with_invalid_page_number(self):
        url: str = self.index_url + "?page=dasd"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].number, 1)

        parser = HTMLParser(response.content)
        rows = parser.css("table tr:not(:first-child)")

        self.assertEqual(len(rows), 10)

    def test_pagination_with_per_page(self):
        url: str = self.index_url + "?page=1&per_page=50"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].number, 1)

        parser = HTMLParser(response.content)
        rows = parser.css("table tr:not(:first-child)")

        self.assertEqual(len(rows), 50)

    def test_pagination_with_per_page_all_and_invalid_page_number(self):
        url: str = self.index_url + "?page=dasd&per_page=all"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].number, 1)

        parser = HTMLParser(response.content)
        rows = parser.css("table tr:not(:first-child)")

        self.assertEqual(len(rows), 300)

    def test_pagination_with_per_page_and_page_number_over_the_pages_count(self):
        url: str = self.index_url + "?page=12&per_page=100"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].number, 3)

        parser = HTMLParser(response.content)
        rows = parser.css("table tr:not(:first-child)")

        self.assertEqual(len(rows), 100)
