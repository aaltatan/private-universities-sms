from datetime import datetime

import pytest
from django.test import Client

from tests.utils import load_yaml


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["export"],
)
def test_export_response(
    admin_client: Client,
    urls: dict[str, str],
    headers_modal_GET: dict[str, str],
    filename: str,
    params: dict,
) -> None:
    url = urls["index"] + f"?export=true&extension={params['extension']}"

    response = admin_client.get(url, headers=headers_modal_GET)

    assert response.status_code == 200
    assert "HX-Redirect" in response.headers

    url += "&redirected=true"
    response = admin_client.get(url, headers=headers_modal_GET)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == params["content_type"]

    str_now_without_sec = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename_without_sec = f"{filename}-{str_now_without_sec}"

    assert filename_without_sec in response.headers["Content-Disposition"]
