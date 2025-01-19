import json
import re

import pytest
import pytest_mock
from django.contrib import messages
from django.test import Client
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_delete_perm(
    admin_client: Client,
    urls: dict[str, str],
) -> None:
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("a[aria-label='delete object']")

    assert response.status_code == 200
    assert btn is not None


@pytest.mark.django_db
def test_delete_object_if_headers_has_no_hx_request(
    admin_client: Client, model: type[Model]
) -> None:
    obj = model.objects.first()
    response = admin_client.post(
        obj.get_delete_url(),
    )
    messages_list = list(
        messages.get_messages(response.wsgi_request),
    )

    assert response.status_code == 404
    assert messages_list[0].level == messages.ERROR
    assert (
        messages_list[0].message
        == "you can't delete this object because you are not using htmx."
    )


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_no_delete_perm(
    client: Client, urls: dict[str, str], model: type[Model]
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
    model: type[Model], admin_client: Client
) -> None:
    obj = model.objects.first()
    response = admin_client.get(obj.get_delete_url())
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_delete_modal_with_using_htmx(
    model: type[Model],
    admin_client: Client,
    templates: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    obj = model.objects.first()

    response = admin_client.get(
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
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
) -> None:
    obj = model.objects.first()
    response = admin_client.post(
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
    assert messages_list[0].message == f"{obj.name} has been deleted successfully."
    assert model.objects.count() == 303


@pytest.mark.django_db
def test_delete_object_undeletable(
    model: type[Model],
    admin_client: Client,
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
) -> None:
    mocker.patch(
        f"apps.{app_label}.utils.Deleter.is_obj_deletable",
        return_value=False,
    )

    obj = model.objects.first()
    response = admin_client.post(
        obj.get_delete_url(),
        headers=headers_modal_GET,
    )
    messages_list = list(
        messages.get_messages(response.wsgi_request),
    )

    assert response.status_code == 200
    assert response.headers.get("Hx-Location") is None
    assert response.headers.get("Hx-Retarget") == "#no-content"
    assert response.headers.get("HX-Reswap") == "innerHTML"
    assert response.headers.get("Hx-Trigger") == "messages"
    assert messages_list[0].level == messages.ERROR
    assert messages_list[0].message == f"{obj.name} cannot be deleted."
    assert model.objects.count() == 304


@pytest.mark.django_db
def test_delete_when_no_deleter_class_is_defined(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(f"apps.{app_label}.views.DeleteView.deleter", new=None)
    obj = model.objects.first()
    with pytest.raises(AttributeError):
        admin_client.post(
            obj.get_delete_url(),
            headers=headers_modal_GET,
        )


@pytest.mark.django_db
def test_delete_when_deleter_class_is_not_subclass_of_Deleter(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    class Deleter: ...

    mocker.patch(f"apps.{app_label}.views.DeleteView.deleter", new=Deleter)
    obj = model.objects.first()
    with pytest.raises(TypeError):
        admin_client.post(
            obj.get_delete_url(),
            headers=headers_modal_GET,
        )
