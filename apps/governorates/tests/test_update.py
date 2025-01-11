import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.contrib.messages import get_messages

from selectolax.parser import HTMLParser

from apps.core.models import User

from ..models import Governorate
from .constants import DIRTY_DATA


class GovernorateUpdateTest(TestCase):
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
        delete_perm = Permission.objects.get(
            codename="delete_governorate",
        )
        user_with_view_perm_only.user_permissions.add(
            view_perm,
            delete_perm,
        )

        for idx in range(1, 5):
            Governorate.objects.create(
                name=f"Governorate {idx}",
                description=f"Description {idx}",
            )

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.app_label = self.model._meta.app_label

        self.index_url = reverse("governorates:index")

        self.update_template = "apps/governorates/update.html"
        self.update_modal_form_template = "components/app-forms/modal-update.html"

        self.clean_data_sample = {
            "name": "Governorate 10",
            "description": "googlexxx",
        }

    def test_index_page_has_update_links_for_authorized_user(
        self,
    ) -> None:
        url = self.index_url
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        tds_name = parser.css("td[data-header='name'] a")

        self.assertEqual(len(tds_name), 4)

        for pk, td in enumerate(tds_name, 1):
            update_url = self.model.objects.get(pk=pk).get_update_url()
            self.assertEqual(update_url, td.attributes["hx-get"])

        edit_context_menu_btns = parser.css(
            "li a[aria-label='edit object']",
        )

        self.assertEqual(len(edit_context_menu_btns), 4)

        for pk, btn in enumerate(edit_context_menu_btns, 1):
            update_url = self.model.objects.get(pk=pk).get_update_url()
            self.assertEqual(update_url, btn.attributes["href"])

        context_menu_btns = parser.css(
            "table li[role='menuitem']",
        )

        self.assertEqual(len(context_menu_btns), 8)

    def test_index_page_has_no_update_links_for_unauthorized_user(
        self,
    ) -> None:
        self.client.logout()
        self.client.login(username="user", password="user")

        url = self.index_url
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        tds_name = parser.css("td[data-header='name'] a")
        edit_context_menu_btns = parser.css(
            "li a[aria-label='edit object']",
        )

        self.assertEqual(len(tds_name), 0)
        self.assertEqual(len(edit_context_menu_btns), 0)

        tds_name = parser.css("td[data-header='name']")

        for pk, td in enumerate(tds_name, 1):
            update_url = self.model.objects.get(pk=pk).name
            self.assertEqual(update_url, td.text(strip=True))

        delete_context_menu_btns = parser.css(
            "table li[role='menuitem']",
        )

        self.assertEqual(len(delete_context_menu_btns), 4)

        url = self.model.objects.first().get_update_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_update_page(self):
        obj = self.model.objects.first()

        url = obj.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.update_template)

        parser = HTMLParser(response.content)

        h1 = parser.css_first("form h1").text(strip=True)

        self.assertEqual(h1, f"update {obj.name}")

        form = parser.css_first("main form")

        self.assertEqual(
            form.attributes["hx-post"],
            obj.get_update_url(),
        )
        self.assertEqual(
            form.attributes["id"],
            f"{self.app_label}-form",
        )

        name_input = form.css_first("input[name='name']")
        description_input = form.css_first(
            "textarea[name='description']",
        )

        self.assertEqual(name_input.attributes["value"], obj.name)
        self.assertEqual(
            description_input.text(strip=True),
            obj.description,
        )

        required_star = form.css_first(
            "span[aria-label='required field']",
        )

        self.assertIsNotNone(required_star)

    def test_update_form_has_previous_page_querystring(self):
        obj = self.model.objects.first()

        url = obj.get_update_url() + "?page=1&per_page=10&order_by=-Id"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        parser = HTMLParser(response.content)

        form = parser.css_first("main form")

        self.assertEqual(form.attributes["hx-post"], url)

    def update_with_dirty_data(self):
        obj = self.model.objects.first()
        url = obj.get_update_url()

        for data in DIRTY_DATA:
            response = self.client.post(url, data["data"])
            self.assertContains(response, data["error"])
            self.assertTemplateUsed(
                response,
                "components/app-forms/update.html",
            )
            self.assertEqual(response.status_code, 200)

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 4)

    def update_with_modal_with_dirty_data(self):
        obj = self.model.objects.first()
        url = obj.get_update_url() + "?page=1&per_page=10&order_by=-Id"

        headers = {
            "modal": True,
            "redirect-to": self.index_url,
            "querystring": "page=1&per_page=10&order_by=-Id",
        }

        for data in DIRTY_DATA:
            response = self.client.post(
                url,
                data["data"],
                headers=headers,
            )
            self.assertContains(response, data["error"])
            self.assertTemplateUsed(
                response,
                "components/app-forms/modal-update.html",
            )
            self.assertEqual(response.status_code, 200)

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 4)

    def test_update_form_with_clean_data(self):
        querystring = "?page=1&per_page=10&order_by=-Id"
        obj = self.model.objects.first()
        url = obj.get_update_url() + querystring

        response = self.client.post(url, self.clean_data_sample)
        self.assertEqual(response.status_code, 200)

        messages_list = list(
            get_messages(request=response.wsgi_request),
        )

        self.assertEqual(messages_list[0].level, messages.SUCCESS)

        name = self.clean_data_sample["name"]
        description = self.clean_data_sample["description"]

        self.assertEqual(
            messages_list[0].message,
            f"({name}) has been updated successfully",
        )

        self.assertEqual(
            response.headers.get("Hx-redirect"),
            self.index_url + querystring,
        )

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 4)

        obj = self.model.objects.first()

        self.assertEqual(obj.name, name)
        self.assertEqual(obj.description, description)

    def test_update_with_redirect_from_modal(
        self,
    ) -> None:
        obj = self.model.objects.first()
        url = obj.get_update_url() + "?per_page=10&order_by=-Id"

        headers = {
            "Hx-Request": "true",
            "modal": True,
            "redirect-to": self.index_url,
            "querystring": "per_page=10&order_by=-Id",
        }

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            self.update_modal_form_template,
        )

        parser = HTMLParser(response.content)

        form = parser.css_first("form")
        form_hx_post = form.attributes.get("hx-post")

        self.assertEqual(form_hx_post, url)

        response = self.client.post(
            url,
            self.clean_data_sample,
            headers=headers,
        )

        location = json.loads(
            response.headers.get("Hx-Location", ""),
        )
        location_path = location.get("path")

        self.assertEqual(
            location_path,
            self.index_url + "per_page=10&order_by=-Id",
        )

        messages_list = list(
            get_messages(request=response.wsgi_request),
        )

        self.assertEqual(messages_list[0].level, messages.SUCCESS)

        name = self.clean_data_sample["name"]
        description = self.clean_data_sample["description"]

        self.assertEqual(
            messages_list[0].message,
            f"({name}) has been updated successfully",
        )

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 4)

        obj = self.model.objects.first()

        self.assertEqual(obj.name, name)
        self.assertEqual(obj.description, description)

    def test_update_without_redirect_from_modal(
        self,
    ) -> None:
        obj = self.model.objects.first()
        url = obj.get_update_url() + "?per_page=10&order_by=-Id"

        headers = {
            "Hx-Request": "true",
            "modal": True,
        }

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            self.update_modal_form_template,
        )

        parser = HTMLParser(response.content)

        form = parser.css_first("form")
        form_hx_post = form.attributes.get("hx-post")

        self.assertEqual(form_hx_post, url)

        response = self.client.post(
            url,
            self.clean_data_sample,
            headers=headers,
        )

        self.assertIsNone(response.headers.get("Hx-Location"))

        messages_list = list(
            get_messages(request=response.wsgi_request),
        )

        self.assertEqual(messages_list[0].level, messages.SUCCESS)

        name = self.clean_data_sample["name"]
        description = self.clean_data_sample["description"]

        self.assertEqual(
            messages_list[0].message,
            f"({name}) has been updated successfully",
        )

        qs = self.model.objects.all()

        self.assertEqual(qs.count(), 4)

        obj = self.model.objects.first()

        self.assertEqual(obj.name, name)
        self.assertEqual(obj.description, description)
