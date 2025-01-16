import pytest
from django.test import Client

from apps.core.tests.utils import assert_export


@pytest.mark.django_db
def test_export_response_xlsx(
    super_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
) -> None:
    assert_export(super_client, urls, headers_modal_GET, filename, "xlsx")


@pytest.mark.django_db
def test_export_response_csv(
    super_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
) -> None:
    assert_export(super_client, urls, headers_modal_GET, filename, "csv")


@pytest.mark.django_db
def test_export_response_json(
    super_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
):
    assert_export(super_client, urls, headers_modal_GET, filename, "json")
