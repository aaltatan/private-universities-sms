import json

import pytest
import pytest_mock
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        "?app_label=xx&model=governorate",
        "?app_label=geo&model=xx",
        "?&model=governorate",
        "?app_label=geo",
    ],
)
def test_activities_with_no_wrong_payload(admin_client: Client, payload: str):
    path = reverse("core:activities", args=[1])
    response = admin_client.get(path + payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_activities_with_no_permissions(client: Client):
    client.login(
        username="user_with_no_perm",
        password="password",
    )
    path = reverse("core:activities", args=[1])
    response = client.get(path + "?app_label=geo&model=governorate")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_activities(
    admin_client: Client,
    urls: dict[str, str],
    model: Model,
    activity_model,
):
    payload = {
        "name": "Governorate 10",
        "description": "description",
    }
    data = {**payload, "save": "true"}

    response = admin_client.post(urls["create"], data)
    qs = model.objects.all()
    activity = activity_model.objects.first()
    activities_count = activity_model.objects.count()

    assert response.status_code == 201
    assert qs.count() == 5
    assert activity.kind == "create"
    assert activity.data is None
    assert activity.user.username == "admin"
    assert activities_count == 1

    payload = {"app_label": "geo", "model": "governorate"}
    path = reverse("core:activities", args=[5])

    response = admin_client.get(path=path, data=payload)

    parser = HTMLParser(response.content)
    data_td = parser.css_first(
        "table td[data-header='Data'] pre",
    ).text(strip=True)
    user_td = parser.css_first(
        "table td[data-header='User'] div",
    ).text(strip=True)
    kind_td = parser.css_first(
        "table td[data-header='Kind'] div span",
    ).text(strip=True)

    assert response.status_code == 200
    assert user_td == "admin"
    assert kind_td == "create"
    assert json.loads(data_td) is None


@pytest.mark.django_db
def test_create_api_activities(
    api_client: APIClient,
    admin_headers: dict[str, str],
    urls: dict[str, str],
    model: Model,
    activity_model,
):
    payload = {
        "name": "Governorate 10",
        "description": "description",
    }

    response: Response = api_client.post(
        path=f'{urls["api"]}',
        data=payload,
        headers=admin_headers,
    )
    qs = model.objects.all()
    activity = activity_model.objects.first()
    activities_count = activity_model.objects.count()

    assert response.status_code == 201
    assert qs.count() == 5
    assert activity.kind == "create"
    assert activity.data is None
    assert activity.user.username == "admin"
    assert activities_count == 1


@pytest.mark.django_db
def test_delete_activity(
    admin_client: Client,
    model: Model,
    activity_model,
):
    path = reverse(
        viewname="geo:governorates:delete",
        kwargs={"slug": "محافظة-ادلب"},
    )
    response = admin_client.post(path=path, headers={"hx-request": "true"})

    qs = model.objects.all()
    activity = activity_model.objects.first()

    assert response.status_code == 204
    assert qs.count() == 3
    assert activity.kind == "delete"
    assert activity.data == {"name": "محافظة ادلب", "description": "meta"}
    assert activity.user.username == "admin"


@pytest.mark.django_db
def test_delete_api_activity(
    api_client: APIClient,
    admin_headers: dict[str, str],
    urls: dict[str, str],
    model: Model,
    activity_model,
):
    response = api_client.delete(path=f'{urls["api"]}3/', headers=admin_headers)

    qs = model.objects.all()
    activity = activity_model.objects.first()

    assert response.status_code == 204
    assert qs.count() == 3
    assert activity.kind == "delete"
    assert activity.data == {"name": "محافظة ادلب", "description": "meta"}
    assert activity.user.username == "admin"


@pytest.mark.django_db
def test_update_activity(
    admin_client: Client,
    templates: dict[str, str],
    model: Model,
    mocker: pytest_mock.MockerFixture,
    activity_model,
):
    mocker.patch("apps.geo.views.governorates.UpdateView.inlines", new=None)
    payload = {
        "name": "hamah",
        "description": "google",
    }
    edited_payload = {
        **payload,
        "update": "true",
    }
    response = admin_client.post(
        path=reverse(
            viewname="geo:governorates:update",
            kwargs={"slug": "محافظة-حماه"},
        ),
        headers={"hx-request": "true"},
        data=edited_payload,
    )

    qs = model.objects.all()
    activity = activity_model.objects.first()
    expected_data = {
        "before": {"name": "محافظة حماه", "description": "goo"},
        "after": payload,
    }

    assert response.status_code == 200
    assert qs.count() == 4
    assert activity.kind == "update"
    assert activity.data == expected_data
    assert activity.user.username == "admin"

    payload = {"app_label": "geo", "model": "governorate"}
    path = reverse("core:activities", args=[1])

    response = admin_client.get(path=path, data=payload)

    parser = HTMLParser(response.content)
    data_td = parser.css_first(
        "table td[data-header='Data'] pre",
    ).text(strip=True)
    user_td = parser.css_first(
        "table td[data-header='User'] div",
    ).text(strip=True)
    kind_td = parser.css_first(
        "table td[data-header='Kind'] div span",
    ).text(strip=True)

    assert response.status_code == 200
    assert user_td == "admin"
    assert kind_td == "update"
    assert json.loads(data_td) == expected_data
    assert is_template_used(templates["activities"], response=response)


@pytest.mark.django_db
def test_update_api_activity(
    api_client: APIClient,
    admin_headers: dict[str, str],
    urls: dict[str, str],
    model: Model,
    activity_model,
):
    payload = {
        "name": "hamah",
        "description": "google",
    }
    response = api_client.put(
        path=f'{urls["api"]}1/',
        headers=admin_headers,
        data=payload,
    )

    qs = model.objects.all()
    activity = activity_model.objects.first()

    assert response.status_code == 200
    assert qs.count() == 4
    assert activity.kind == "update"
    assert activity.data == {
        "before": {"name": "محافظة حماه", "description": "goo"},
        "after": payload,
    }
    assert activity.user.username == "admin"


@pytest.mark.django_db
def test_bulk_delete_activity(
    admin_client: Client,
    urls: dict[str, str],
    model: type[Model],
    activity_model,
):
    data: dict = {
        "action_check": list(range(3, 5)),
        "kind": "action",
        "name": "delete",
    }

    response = admin_client.post(urls["index"], data)
    activities = activity_model.objects.all()

    data = [
        {"name": "محافظة ادلب", "description": "meta"},
        {"name": "محافظة المنيا", "description": "language mena"},
    ]

    assert response.status_code == 204
    assert model.objects.count() == 2
    assert activities.count() == 2

    for activity in activities:
        assert activity.kind == "delete"
        assert activity.data in data
        assert activity.user.username == "admin"


@pytest.mark.django_db
def test_bulk_delete_api_activity(
    api_client: APIClient,
    admin_headers: dict[str, str],
    urls: dict[str, str],
    model: type[Model],
    activity_model,
):
    response = api_client.post(
        path=f'{urls["api"]}bulk-delete/',
        data={"ids": list(range(3, 5))},
        headers=admin_headers,
    )
    activities = activity_model.objects.all()

    data = [
        {"name": "محافظة ادلب", "description": "meta"},
        {"name": "محافظة المنيا", "description": "language mena"},
    ]

    assert response.status_code == 204
    assert model.objects.count() == 2
    assert activities.count() == 2

    for activity in activities:
        assert activity.kind == "delete"
        assert activity.data in data
        assert activity.user.username == "admin"
