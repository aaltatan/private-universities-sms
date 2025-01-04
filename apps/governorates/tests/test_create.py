import json
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.contrib import messages

from selectolax.parser import HTMLParser

from apps.core.models import User

from ..models import Governorate
from .constants import DIRTY_DATA


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
        self.dirty_data = DIRTY_DATA

        self.clean_data_sample = {
            "name": "Hamah",
            "description": "google",
            "save": "true",
        }
        self.success_message = (
            f"{self.clean_data_sample['name']} has been created successfully"
        )
        self.headers_modal_GET = {
            "modal": "true",
            "Hx-Request": "true",
        }

        app_label = self.model._meta.app_label

        # urls
        self.index_url = reverse(f"{app_label}:index")
        self.create_url = reverse(f"{app_label}:create")
        # selectors
        self.add_btn_selector = "[aria-label='create new object']"
        # templates
        self.index_template = f"apps/{app_label}/index.html"
        self.create_template = f"apps/{app_label}/create.html"
        self.create_form_template = "components/forms/create.html"
        self.create_modal_form_template = "components/app-forms/modal-create.html"

    def test_add_new_btn_appearance_if_user_has_no_add_perm(
        self,
    ) -> None:
        self.client.logout()
        self.client.login(username="user", password="user")

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        btn = parser.css_first(self.add_btn_selector)

        self.assertTemplateUsed(self.index_template)
        self.assertIsNone(btn)

    def test_send_request_to_create_page_without_permission(
        self,
    ) -> None:
        self.client.logout()
        self.client.login(username="user", password="user")

        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, 403)

    def test_add_new_btn_appearance_if_user_has_add_perm(
        self,
    ) -> None:
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        btn = parser.css_first(self.add_btn_selector)

        self.assertTemplateUsed(self.index_template)
        self.assertIsNotNone(btn)

    def test_send_request_to_create_page_with_permission(
        self,
    ) -> None:
        response = self.client.get(self.create_url)
        self.assertTemplateUsed(self.create_form_template)
        self.assertEqual(response.status_code, 200)

    def test_create_new_object_with_save_btn(self) -> None:
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.create_template)

        response = self.client.post(
            self.create_url,
            self.clean_data_sample,
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.headers.get("Hx-Redirect"))
        self.assertEqual(
            response.headers.get("Hx-Trigger"),
            "messages",
        )

        messages_list = list(
            get_messages(request=response.wsgi_request),
        )
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(
            messages_list[0].message,
            self.success_message,
        )

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 5)

    def test_create_new_object_with_save_and_add_another_btn(
        self,
    ) -> None:
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.create_template)

        data = self.clean_data_sample.copy()
        del data["save"]
        data["save_and_add_another"] = "true"

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.headers.get("Hx-Trigger"),
            "messages",
        )
        self.assertTemplateUsed(response, self.create_form_template)

        qs = self.model.objects.all()

        last_obj = qs.last()

        self.assertEqual(last_obj.pk, 5)
        self.assertEqual(last_obj.name, data["name"])
        self.assertEqual(last_obj.description, data["description"])
        self.assertEqual(
            last_obj.slug,
            slugify(
                data["name"],
                allow_unicode=True,
            ),
        )

        self.assertEqual(qs.count(), 5)

    def test_create_simulating_create_without_redirect_from_modal(
        self,
    ) -> None:
        headers = self.headers_modal_GET

        response = self.client.get(self.create_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            self.create_modal_form_template,
        )

        headers = {
            "modal": True,
        }
        response = self.client.post(
            self.create_url,
            self.clean_data_sample,
            headers=headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertTemplateNotUsed(
            response=response,
            template_name=self.create_form_template,
        )

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 5)

        self.assertIsNone(response.headers.get("Hx-Redirect"))

        messages_list = list(
            get_messages(request=response.wsgi_request),
        )
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(
            messages_list[0].message,
            self.success_message,
        )

    def test_create_simulating_create_with_redirect_from_modal(
        self,
    ) -> None:
        url = self.create_url + "?per_page=10&order_by=-Name"

        headers = self.headers_modal_GET

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            self.create_modal_form_template,
        )

        headers = {
            "modal": True,
            "redirect-to": self.index_url,
            "querystring": "per_page=10&order_by=-Name",
        }
        response = self.client.post(
            url,
            self.clean_data_sample,
            headers=headers,
        )
        self.assertEqual(response.status_code, 201)

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 5)

        location: dict = json.loads(
            response.headers.get("Hx-Location", ""),
        )
        location_path = location.get("path")

        self.assertEqual(
            location_path,
            self.index_url + "per_page=10&order_by=-Name",
        )

        messages_list = list(
            get_messages(request=response.wsgi_request),
        )
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(
            messages_list[0].message,
            self.success_message,
        )

        headers = {
            "modal": True,
            "redirect-to": self.index_url,
        }

        data = self.clean_data_sample.copy()
        data["name"] = "afasfasf"

        response = self.client.post(url, data, headers=headers)
        self.assertEqual(response.status_code, 201)

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 6)

        location: dict = json.loads(
            response.headers.get("Hx-Location", ""),
        )
        location_path = location.get("path")
        self.assertEqual(location_path, self.index_url)

    def test_create_new_object_with_dirty_or_duplicated_data(
        self,
    ) -> None:
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.create_template)

        for data in self.dirty_data:
            response = self.client.post(
                self.create_url,
                data["data"],
            )
            self.assertContains(response, data["error"])
            self.assertTemplateUsed(
                response,
                self.create_form_template,
            )
            self.assertEqual(response.status_code, 200)
            parser = HTMLParser(response.content)
            form_hx_post = parser.css_first("form[hx-post]").attributes.get("hx-post")
            self.assertEqual(form_hx_post, self.create_url)

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 4)

    def test_create_new_object_with_modal_with_dirty_or_duplicated_data(
        self,
    ) -> None:
        url = self.create_url + "?per_page=10&order_by=-Name"

        headers = self.headers_modal_GET

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            self.create_modal_form_template,
        )

        for data in self.dirty_data:
            response = self.client.post(
                url,
                data["data"],
                headers=headers,
            )
            self.assertContains(response, data["error"])
            self.assertTemplateUsed(
                response,
                self.create_modal_form_template,
            )
            self.assertEqual(response.status_code, 200)
            parser = HTMLParser(response.content)
            form_hx_post = parser.css_first(
                "form[hx-post]",
            ).attributes.get("hx-post")
            self.assertEqual(form_hx_post, url)

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 4)
