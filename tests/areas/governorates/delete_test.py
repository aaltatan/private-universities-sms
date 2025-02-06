import json
import re

import pytest
import pytest_mock
from django.contrib import messages
from django.test import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_delete_perm(
    admin_client: Client, urls: dict[str, str]
) -> None:
    response = admin_client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("a[aria-label='delete object']")

    assert response.status_code == status.HTTP_200_OK
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

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert messages_list[0].level == messages.ERROR
    assert (
        messages_list[0].message
        == "you can't delete this object because you are not using htmx."
    )


@pytest.mark.django_db
def test_delete_btn_appearance_if_user_has_no_delete_perm(
    client: Client,
    urls: dict[str, str],
    model: type[Model],
    app_label: str,
) -> None:
    client.login(
        username=f"{app_label}_user_with_view_perm_only",
        password="password",
    )
    response = client.get(urls["index"])
    parser = HTMLParser(response.content)
    btn = parser.css_first("a[aria-label='delete object']")

    assert response.status_code == status.HTTP_200_OK
    assert btn is None

    obj = model.objects.first()
    response = client.get(obj.get_delete_url())

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_delete_modal_without_using_htmx(
    model: type[Model], admin_client: Client
) -> None:
    obj = model.objects.first()
    response = admin_client.get(obj.get_delete_url())
    assert response.status_code == status.HTTP_404_NOT_FOUND


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
    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["delete_modal"], response)


@pytest.mark.django_db
def test_delete_object(
    model: type[Model],
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    counts: dict[str, int],
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

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert location_path == urls["index"]
    assert response.headers.get("Hx-Trigger") == "messages"
    assert messages_list[0].level == messages.SUCCESS
    assert messages_list[0].message == f"{obj.name} has been deleted successfully."
    assert model.objects.count() == counts["objects"] - 1


@pytest.mark.django_db
def test_delete_object_undeletable(
    model: type[Model],
    admin_client: Client,
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    counts: dict[str, int],
) -> None:
    mocker.patch(
        f"apps.geo.{app_label}.utils.Deleter.is_obj_deletable",
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

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("Hx-Location") is None
    assert response.headers.get("Hx-Retarget") == "#no-content"
    assert response.headers.get("HX-Reswap") == "innerHTML"
    assert response.headers.get("Hx-Trigger") == "messages"
    assert messages_list[0].level == messages.ERROR
    assert messages_list[0].message == f"{obj.name} cannot be deleted."
    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_delete_when_no_deleter_class_is_defined(
    admin_client: Client,
    model: type[Model],
    headers_modal_GET: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(f"apps.geo.views.{app_label}.DeleteView.deleter", new=None)
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

    mocker.patch(f"apps.geo.{app_label}.views.DeleteView.deleter", new=Deleter)
    obj = model.objects.first()
    with pytest.raises(TypeError):
        admin_client.post(
            obj.get_delete_url(),
            headers=headers_modal_GET,
        )


@pytest.mark.django_db
def test_api_delete_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    counts: dict[str, int],
):
    for idx in range(1, 11):
        response: Response = api_client.delete(
            path=f"{urls['api']}{idx}/",
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert model.objects.count() == counts["objects"] - 10


@pytest.mark.django_db
def test_delete_object_with_invalid_id(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    model_name: str,
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    response: Response = api_client.get(
        path=f"{urls['api']}312312",
        headers=admin_headers,
        follow=True,
    )
    assert response.json() == {"detail": f"No {model_name} matches the given query."}
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert model.objects.count() == objects_count


@pytest.mark.django_db
def test_delete_and_bulk_delete_object_when_deleter_class_is_None(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(f"apps.geo.{app_label}.views.APIViewSet.deleter", new=None)

    with pytest.raises(AttributeError):
        api_client.delete(
            path=f"{urls['api']}1/",
            headers=admin_headers,
        )

    with pytest.raises(AttributeError):
        api_client.post(
            path=f"{urls['api']}bulk-delete/",
            data={"ids": [1, 2, 3, 4, 500, 501]},
            headers=admin_headers,
        )


@pytest.mark.django_db
def test_delete_and_bulk_delete_object_when_deleter_class_is_not_a_subclass_of_Deleter(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    class Deleter:
        pass

    mocker.patch(f"apps.geo.{app_label}.views.APIViewSet.deleter", new=Deleter)

    with pytest.raises(TypeError):
        api_client.delete(
            path=f"{urls['api']}1/",
            headers=admin_headers,
        )

    with pytest.raises(TypeError):
        api_client.post(
            path=f"{urls['api']}bulk-delete/",
            data={"ids": [1, 2, 3, 4, 500, 501]},
            headers=admin_headers,
        )


@pytest.mark.django_db
@pytest.mark.parametrize("idx", list(range(1, 11)))
def test_api_delete_object_undeletable(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    idx: int,
    counts: dict[str, int],
):
    objects_count = counts["objects"]
    mocker.patch(
        f"apps.geo.{app_label}.utils.Deleter.is_obj_deletable",
        return_value=False,
    )

    response: Response = api_client.delete(
        path=f"{urls['api']}{idx}/",
        headers=admin_headers,
    )

    assert model.objects.count() == objects_count
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["details"].endswith("cannot be deleted.")
