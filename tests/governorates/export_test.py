import pytest
from django.test import Client

from tests.utils import assert_export


@pytest.mark.django_db
def test_export_response_xlsx(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
) -> None:
    assert_export(admin_client, urls, headers_modal_GET, filename, "xlsx")


@pytest.mark.django_db
def test_export_response_csv(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
) -> None:
    assert_export(admin_client, urls, headers_modal_GET, filename, "csv")


@pytest.mark.django_db
def test_export_response_json(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
):
    assert_export(admin_client, urls, headers_modal_GET, filename, "json")
