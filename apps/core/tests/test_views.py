from django.test import TestCase
from django.urls import reverse

from ..models import User


class IndexViewTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test", password="test")
    
    def test_index_without_authentication_view(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 302)
    
    def test_index_authentication_view(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("core:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/core/index.html")
    
