import re
import json

import pytest
import pytest_mock
from django.test import Client
from django.contrib import messages
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_bulk_delete_modal_response(
    admin_client: Client,
    urls: dict[str, str],
):
    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "modal",
        "name": "delete",
    }
    response = admin_client.post(urls["index"], data)
    parser = HTMLParser(response.content)
    modal_body = (
        parser.css_first(
            "#modal-container > div > form > div:nth-child(2) p",
        )
        .text(strip=True)
        .replace("\n", "")
        .strip()
    )
    modal_body = re.compile(r"\s{2,}").sub(" ", modal_body)

    assert response.status_code == 200
    assert modal_body == "are you sure you want to delete all 50 selected objects ?"


@pytest.mark.django_db
def test_bulk_delete_without_permissions(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )

    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "delete",
    }

    response = client.post(urls["index"], data, follow=True)
    assert response.status_code == 403


@pytest.mark.django_db
def test_bulk_delete_with_permissions(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
):
    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "delete",
    }

    response = admin_client.post(urls["index"], data)
    hx_location = json.loads(
        response.headers.get("Hx-Location"),
    )
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )

    assert response.status_code == 204
    assert response.headers.get("Hx-Location") is not None
    assert hx_location["path"] == urls["index"]
    assert messages_list[0].level == messages.SUCCESS
    assert (
        messages_list[0].message
        == "all selected 50 objects have been deleted successfully."
    )
    assert model.objects.count() == 254


@pytest.mark.django_db
def test_bulk_delete_with_permissions_with_undeletable_objects(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "delete",
    }

    mocker.patch(
        f"apps.{app_label}.utils.Deleter.is_qs_deletable",
        return_value=False,
    )

    response = admin_client.post(urls["index"], data)
    messages_list = list(
        messages.get_messages(request=response.wsgi_request),
    )

    assert response.status_code == 200
    assert response.headers.get("Hx-Location") is None
    assert response.headers.get("Hx-Retarget") == "#no-content"
    assert response.headers.get("HX-Reswap") == "innerHTML"
    assert response.headers.get("HX-Trigger") == "messages"
    assert messages_list[0].level == messages.ERROR
    assert messages_list[0].message == "selected 50 objects cannot be deleted."
    assert model.objects.count() == 304


@pytest.mark.django_db
def test_bulk_action_not_found(
    admin_client: Client,
    urls: dict[str, str],
):
    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "bulk_delete",  # name not in actions
    }

    response = admin_client.post(urls["index"], data)
    assert response.status_code == 500

    response = admin_client.post(urls["index"], data, follow=True)
    assert response.status_code == 500


@pytest.mark.django_db
def test_bulk_delete_with_permissions_only_for_view(
    client: Client,
    urls: dict[str, str],
):
    client.login(
        username="user_with_view_perm_only",
        password="user_with_view_perm_only",
    )

    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "delete",
    }

    response = client.post(urls["index"], data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_bulk_delete_when_no_deleter_class_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(f"apps.{app_label}.views.ListView.deleter", new=None)
    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "delete",
    }
    with pytest.raises(AttributeError):
        admin_client.post(urls["index"], data)


@pytest.mark.django_db
def test_bulk_delete_when_deleter_class_is_not_subclass_of_Deleter(
    admin_client: Client,
    urls: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    class Deleter: ...

    mocker.patch(f"apps.{app_label}.views.ListView.deleter", new=Deleter)
    data: dict = {
        "action-check": list(range(1, 51)),
        "kind": "action",
        "name": "delete",
    }
    with pytest.raises(TypeError):
        admin_client.post(urls["index"], data)
