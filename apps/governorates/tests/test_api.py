from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.response import Response

from apps.core.models import User

from ..models import Governorate


class GovernorateTest(TestCase):
    model = Governorate

    @classmethod
    def setUpTestData(cls):
        client = Client()

        cls.api_client = APIClient()

        cls.base_url = "/api/governorates/"

        User.objects.create_superuser(
            username="admin",
            password="admin",
        )
        response = client.post(
            "/api/token/", {"username": "admin", "password": "admin"}
        )
        admin_token = response.json()["access"]
        cls.admin_headers = {
            "Authorization": f"Bearer {admin_token}",
        }

        User.objects.create_user(
            username="user",
            password="user",
        )
        response = client.post(
            "/api/token/",
            {"username": "user", "password": "user"},
        )
        user_token = response.json()["access"]
        cls.user_headers = {
            "Authorization": f"Bearer {user_token}",
        }

        cls.model_name = Governorate._meta.model_name.title()

        cls.dirty_data = [
            {
                "data": {"name": "Ci"},
                "error": ["Ensure this field has at least 4 characters."],
                "status_code": 400,
            },
            {
                "data": {"name": ""},
                "error": ["This field may not be blank."],
                "status_code": 400,
            },
            {
                "data": {"name": "a" * 265},
                "error": ["Ensure this field has no more than 255 characters."],
                "status_code": 400,
            },
            {
                "data": {"name": "City 1"},
                "error": ["governorate with this name already exists."],
                "status_code": 400,
            },
        ]

        for idx in range(1, 41):
            cls.model.objects.create(
                name=f"City {idx}",
            )

    def test_read_objects(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}",
            headers=self.admin_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 40)
        self.assertEqual(len(response.json()["results"]), 10)

    def test_filter_objects_using_q(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}?q=City+4",
            headers=self.admin_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        for idx in (4, 14, 24, 34, 40):
            self.assertIn(
                {
                    "id": idx,
                    "name": f"City {idx}",
                    "description": "",
                    "slug": f"city-{idx}",
                },
                response.json()["results"],
            )
        self.assertEqual(response.json()["count"], 5)

    def test_filter_objects_using_djangoql(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}?q=id<4",
            headers=self.admin_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        for idx in range(1, 4):
            self.assertIn(
                {
                    "id": idx,
                    "name": f"City {idx}",
                    "description": "",
                    "slug": f"city-{idx}",
                },
                response.json()["results"],
            )
        self.assertEqual(response.json()["count"], 3)

    def test_filter_objects_using_djangoql_endswith(self):
        response: Response = self.api_client.get(
            path=f'{self.base_url}?q=name endswith "3"',
            headers=self.admin_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        for idx in (3, 13, 23, 33):
            self.assertIn(
                {
                    "id": idx,
                    "name": f"City {idx}",
                    "description": "",
                    "slug": f"city-{idx}",
                },
                response.json()["results"],
            )
        self.assertEqual(response.json()["count"], 4)

    def test_delete_object(self):
        for idx in range(1, 11):
            response: Response = self.api_client.delete(
                path=f"{self.base_url}{idx}/",
                headers=self.admin_headers,
                format="json",
            )
            self.assertEqual(response.status_code, 204)

        count = self.model.objects.count()
        self.assertEqual(count, 30)

        response: Response = self.api_client.get(
            path=f"{self.base_url}312312",
            headers=self.admin_headers,
            format="json",
            follow=True,
        )
        self.assertEqual(
            response.json(),
            {"detail": f"No {self.model_name} matches the given query."},
        )
        self.assertEqual(response.status_code, 404)

        count = self.model.objects.count()
        self.assertEqual(count, 30)

    def test_bulk_delete_objects(self):
        response: Response = self.api_client.post(
            path=f"{self.base_url}bulk-delete/",
            data={"ids": [1, 2, 3, 4, 500, 501]},
            headers=self.admin_headers,
            format="json",
        )

        self.assertEqual(response.status_code, 204)

        count = self.model.objects.count()
        self.assertEqual(count, 36)

        response: Response = self.api_client.post(
            path=f"{self.base_url}bulk-delete/",
            data={"ids": [500, 501]},
            headers=self.admin_headers,
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        count = self.model.objects.count()
        self.assertEqual(count, 36)

    def test_read_objects_without_permissions(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}",
            headers=self.user_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_read_object(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}{self.model.objects.first().pk}/",
            headers=self.admin_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "City 1")

    def test_read_object_without_permissions(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}1/",
            headers=self.user_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_read_object_with_invalid_id(self):
        response: Response = self.api_client.get(
            path=f"{self.base_url}4123/",
            headers=self.admin_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_update_object(self):
        response: Response = self.api_client.put(
            path=f"{self.base_url}1/",
            data={
                "name": "Hamah",
                "description": "some description",
            },
            headers=self.admin_headers,
            format="json",
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Hamah")
        self.assertEqual(
            response.json()["description"],
            "some description",
        )

        first = self.model.objects.get(id=1)
        self.assertEqual(first.name, "Hamah")
        self.assertEqual(first.description, "some description")

    def test_update_object_with_dirty_data(self):

        for data in self.dirty_data:
            response: Response = self.api_client.put(
                path=f"{self.base_url}3/",
                data=data['data'],
                headers=self.admin_headers,
                format='json',
            )
            self.assertEqual(
                response.status_code,
                data["status_code"],
            )
            self.assertEqual(response.json()["name"], data["error"])

    def test_create_objects(self):
        for idx in range(41, 51):
            response = self.api_client.post(
                path=self.base_url,
                data={"name": f"City {idx}"},
                headers=self.admin_headers,
                format="json",
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["name"], f"City {idx}")

        response: Response = self.api_client.get(
            path=f"{self.base_url}",
            headers=self.admin_headers,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 50)

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 50)

    def test_create_object_without_permissions(self):
        response = self.api_client.post(
            path=self.base_url,
            data={"name": "City"},
            headers=self.user_headers,
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        response: Response = self.api_client.post(
            path=self.base_url,
            data={"name": "City"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_create_object_with_dirty_data(self):

        for data in self.dirty_data:
            response: Response = self.api_client.post(
                path=self.base_url,
                data=data["data"],
                headers=self.admin_headers,
                format="json",
            )
            self.assertEqual(
                response.status_code,
                data["status_code"],
            )
            self.assertEqual(response.json()["name"], data["error"])
