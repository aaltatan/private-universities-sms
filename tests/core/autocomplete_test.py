from urllib.parse import urlencode

import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from tests.utils import is_template_used


@pytest.mark.django_db
def test_autocomplete_post_method_with_name_as_label_field_name(
    admin_client: Client, urls: dict[str, str]
) -> None:
    payload = {
        "app_label": "geo",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
        "label_field_name": "name",
    }
    querystring = urlencode(payload)
    response = admin_client.post(f"{urls['autocomplete']}1/?{querystring}")

    assert response.status_code == 200
    assert response.json()["value"] == "محافظة حماه"


@pytest.mark.django_db
def test_autocomplete_post_method_with_pk_as_label_field_name(
    admin_client: Client, urls: dict[str, str]
) -> None:
    payload = {
        "app_label": "geo",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
        # "label_field_name": "pk", like default
    }
    querystring = urlencode(payload)
    response = admin_client.post(f"{urls['autocomplete']}1/?{querystring}")

    assert response.status_code == 200
    assert response.json()["value"] == 1


@pytest.mark.django_db
def test_autocomplete_post_method_with_wrong_pk(
    admin_client: Client, urls: dict[str, str]
) -> None:
    payload = {
        "app_label": "geo",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    querystring = urlencode(payload)
    response = admin_client.post(f"{urls['autocomplete']}1312/?{querystring}")

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "term, expected_count",
    [
        ("حم", 2),
        ("محافظة حماه", 1),
        ("محافظة حمص", 1),
        ("xx", 0),
    ],
)
def test_autocomplete(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
    term: str,
    expected_count: int,
):
    payload = {
        "term": term,
        "app_label": "geo",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(urls["autocomplete"], payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li button[role='option']")

    assert len(lis) == expected_count
    assert is_template_used(templates["autocomplete-item"], response)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, status_code",
    [
        (
            {
                "term": "حم",
                # "app_label": "geo",
                "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "name",
            },
            400,
        ),
        (
            {
                "term": "حم",
                "app_label": "geo",
                # "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "name",
            },
            400,
        ),
        (
            {
                "term": "حم",
                "app_label": "geo",
                "model_name": "Governorate",
                "object_name": "governorate",
                # "field_name": "name",
            },
            400,
        ),
        (
            {
                "term": "حم",
                "app_label": "geo",
                "model_name": "Governorate",
                # "object_name": "governorate",
                "field_name": "name",
            },
            400,
        ),
        (
            {
                "term": "حم",
                "app_label": "geo",
                "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "namexx",  # wrong field name
            },
            400,
        ),
        (
            {
                "term": "حم",
                "app_label": "geox",  # wrong app label
                "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "name",
            },
            404,
        ),
        (
            {
                "term": "حم",
                "app_label": "geo",
                "model_name": "Governoratef",  # wrong model name
                "object_name": "governorate",
                "field_name": "name",
            },
            404,
        ),
    ],
)
def test_autocomplete_with_dirty_payload(
    admin_client: Client,
    urls: dict[str, str],
    payload: dict[str, str],
    status_code: int,
):
    response = admin_client.get(urls["autocomplete"], payload)
    assert response.status_code == status_code
