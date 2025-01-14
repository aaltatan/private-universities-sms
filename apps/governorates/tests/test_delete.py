import json
import re

import pytest
from django.contrib import messages
from django.test import Client
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_delete_perm(
    super_client: Client,
    urls: dict[str, str],
) -> None:
    response = super_client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("a[aria-label='delete object']")

    assert response.status_code == 200
    assert btn is not None


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_no_delete_perm(
    client: Client,
    urls: dict[str, str],
    model: type[Model],
) -> None:
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("a[aria-label='delete object']")

    assert response.status_code == 200
    assert btn is None

    obj = model.objects.first()
    response = client.get(obj.get_delete_url())

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_delete_modal_without_using_htmx(
    model: type[Model], super_client: Client
) -> None:
    obj = model.objects.first()
    response = super_client.get(obj.get_delete_url())
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_delete_modal_with_using_htmx(
    model: type[Model],
    super_client: Client,
    templates: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    obj = model.objects.first()

    response = super_client.get(
        obj.get_delete_url(),
        headers=headers_modal_GET,
    )
    parser = HTMLParser(response.content)
    modal_body = parser.css_first(
        "#modal-container p",
    ).text(strip=True)

    modal_body = re.sub(r"\s+", " ", modal_body)

    assert modal_body == f"are you sure you want to delete {obj.name} ?"
    assert response.status_code == 200
    assert templates["delete_modal"] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_delete_object(
    model: type[Model],
    super_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    obj = model.objects.first()
    response = super_client.post(
        obj.get_delete_url(),
        headers=headers_modal_GET,
    )
    location = json.loads(
        response.headers.get("Hx-Location", {}),
    )
    location_path = location.get("path", "")
    messages_list = list(
        messages.get_messages(response.wsgi_request),
    )

    assert response.status_code == 204
    assert location_path == urls["index"]
    assert response.headers.get("Hx-Trigger") == "messages"
    assert messages_list[0].level == messages.SUCCESS
    assert model.objects.count() == 3
