import pytest
import pytest_mock
from django.test import Client

from apps.core.models import AbstractUniqueNameModel as Model

from tests.common import mixins


@pytest.mark.django_db
def test_list_view_with_model_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
    model: type[Model],
):
    mixins.test_list_view_with_model_is_defined(
        admin_client, urls, templates, mocker, app_label, subapp_label, model
    )


@pytest.mark.django_db
def test_list_view_with_template_name_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    mixins.test_list_view_with_template_name_is_defined(
        admin_client, urls, templates, mocker, app_label, subapp_label
    )


@pytest.mark.django_db
def test_list_view_with_table_template_name_is_defined(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    subapp_label: str,
):
    mixins.test_list_view_with_table_template_name_is_defined(
        admin_client, urls, templates, mocker, app_label, subapp_label
    )
