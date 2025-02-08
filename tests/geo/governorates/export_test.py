import pytest
from django.test import Client

from tests.common import export


@pytest.mark.django_db
def test_export_response(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
    export_test_cases: tuple[str, str],
) -> None:
    export.test_export_response(
        admin_client, urls, headers_modal_GET, filename, export_test_cases
    )
