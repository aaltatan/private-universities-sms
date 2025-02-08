import pytest_mock
from django.test import Client
from rest_framework import status

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import is_template_used


def test_list_view_with_model_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
    model: type[Model],
):
    mocker.patch(f"apps.{app_label}.views.{subapp_label}.ListView.model", new=model)
    response = admin_client.get(urls["index"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)


def test_list_view_with_template_name_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    template_name: str = f"apps/{subapp_label}/index.html"
    mocker.patch(
        f"apps.{app_label}.views.{subapp_label}.ListView.template_name",
        new=template_name,
        create=True,
    )
    response = admin_client.get(urls["index"])

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["index"], response)


def test_list_view_with_table_template_name_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    template_name: str = f"components/{subapp_label}/table.html"
    mocker.patch(
        f"apps.{app_label}.views.{subapp_label}.ListView.table_template_name",
        new=template_name,
        create=True,
    )
    response = admin_client.get(
        urls["index"],
        headers={"HX-Request": "true"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert is_template_used(templates["table"], response)
