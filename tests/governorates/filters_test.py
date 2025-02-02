import pytest
from django.test import Client

from tests.utils import get_test_cases


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    get_test_cases("filters.yaml", "governorates"),
)
def test_filters(admin_client: Client, urls: dict[str, str], params: dict):
    url: str = urls["index"] + params["querystring"]
    response = admin_client.get(url)

    assert response.status_code == 200

    for item in params["data"]:
        name, exists = item
        if exists:
            assert name in response.content.decode()
        else:
            assert name not in response.content.decode()

    assert response.context["page"].paginator.count == params["results_count"]
