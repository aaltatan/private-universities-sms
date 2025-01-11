from django.test import TestCase
from django.urls import reverse

from apps.core.models import User

from .. import models


class TestGovernorateFilter(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username="admin",
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

        cls.index_url = reverse("governorates:index")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_view_filter_simple_keyword_search(self):
        url: str = self.index_url + "?q=goo"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hamah")
        self.assertNotContains(response, "Halab")
        self.assertNotContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 1)

    def test_view_filter_for_all_objects_contains_ha_letters(self):
        url: str = self.index_url + "?q=Ha"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hamah")
        self.assertContains(response, "Halab")
        self.assertNotContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 2)

    def test_view_filter_for_all_objects_contains_meta_letters(self):
        url: str = self.index_url + "?q=meta"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Hamah")
        self.assertNotContains(response, "Halab")
        self.assertContains(response, "Homs")
        self.assertContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 2)

    def test_view_filter_with_reversed_keywords(self):
        url: str = self.index_url + "?q=language+halab"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Halab")
        self.assertNotContains(response, "Hamah")
        self.assertNotContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 1)

    def test_view_filter_all_objects_which_id_more_than_2(self):
        url: str = self.index_url + "?q=id > 2"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Hamah")
        self.assertNotContains(response, "Halab")
        self.assertContains(response, "Homs")
        self.assertContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 2)

    def test_view_filter_all_objects_which_id_more_than_2_and_ends_with_us(self):
        url: str = self.index_url + '?q=id > 2 and name endswith "us"'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Hamah")
        self.assertNotContains(response, "Halab")
        self.assertNotContains(response, "Homs")
        self.assertContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 1)

    def test_view_filter_all_objects_which_id_in_one_or_three(self):
        url: str = self.index_url + "?q=id in (1, 3)"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hamah")
        self.assertNotContains(response, "Halab")
        self.assertContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 2)

    def test_view_filter_using_parts_of_words(self):
        url: str = self.index_url + "?q=langu hala"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Halab")
        self.assertNotContains(response, "Hamah")
        self.assertNotContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 1)

    def test_view_filter_with_name(self):
        url: str = self.index_url + "?name=Hamah"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hamah")
        self.assertNotContains(response, "Halab")
        self.assertNotContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 1)

    def test_view_filter_with_description(self):
        url: str = self.index_url + "?description=go language"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Hamah")
        self.assertContains(response, "Halab")
        self.assertNotContains(response, "Homs")
        self.assertNotContains(response, "Damascus")
        self.assertEqual(response.context["page"].paginator.count, 1)
