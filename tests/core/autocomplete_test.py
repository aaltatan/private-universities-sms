from urllib.parse import urlencode

import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from tests.utils import is_template_used


@pytest.mark.django_db
def test_autocomplete_without_permissions(
    client: Client,
    urls: dict[str, str],
) -> None:
    client.login(
        username="user_with_no_perm",
        password="password",
    )
    payload = {
        "term": "حم",
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = client.get(urls["autocomplete"], payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_autocomplete_post_method_with_name_as_label_field_name(
    admin_client: Client,
    urls: dict[str, str],
) -> None:
    payload = {
        "app_label": "areas",
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
    admin_client: Client,
    urls: dict[str, str],
) -> None:
    payload = {
        "app_label": "areas",
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
def test_autocomplete_post_method_without_permissions(
    client: Client,
    urls: dict[str, str],
) -> None:
    client.login(
        username="user_with_no_perm",
        password="password",
    )
    payload = {
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    querystring = urlencode(payload)
    response = client.post(f"{urls['autocomplete']}1/?{querystring}")

    assert response.status_code == 403


@pytest.mark.django_db
def test_autocomplete_post_method_with_wrong_model_name(
    admin_client: Client,
    urls: dict[str, str],
) -> None:
    payload = {
        "app_label": "areas",
        "model_name": "Governoratex",
        "object_name": "governorate",
        "field_name": "name",
    }
    querystring = urlencode(payload)
    response = admin_client.post(f"{urls['autocomplete']}1/?{querystring}")

    assert response.status_code == 404


@pytest.mark.django_db
def test_autocomplete_post_method_with_wrong_pk(
    admin_client: Client,
    urls: dict[str, str],
) -> None:
    payload = {
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    querystring = urlencode(payload)
    response = admin_client.post(f"{urls['autocomplete']}1312/?{querystring}")

    assert response.status_code == 404


@pytest.mark.django_db
def test_autocomplete(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    payload = {
        "term": "حم",
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(urls["autocomplete"], payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")
    for li in lis:
        assert li.text(strip=True) in [
            "محافظة حماه",
            "محافظة حمص",
        ]

    assert is_template_used(templates["autocomplete-item"], response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_autocomplete_with_djangoql(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    payload = {
        "term": 'name endswith "ص"',
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(urls["autocomplete"], payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")
    for li in lis:
        assert li.text(strip=True) in [
            "محافظة حمص",
        ]

    assert len(lis) == 1
    assert is_template_used(templates["autocomplete-item"], response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_autocomplete_with_no_permissions(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    payload = {
        "term": "حم",
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(urls["autocomplete"], payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")
    for li in lis:
        assert li.text(strip=True) in [
            "محافظة حماه",
            "محافظة حمص",
        ]

    assert is_template_used(templates["autocomplete-item"], response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_autocomplete_with_empty_term(
    admin_client: Client,
    urls: dict[str, str],
    templates: dict[str, str],
):
    payload = {
        "term": "xx",
        "app_label": "areas",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(urls["autocomplete"], payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")

    assert len(lis) == 1
    assert is_template_used(templates["autocomplete-item"], response)
    assert parser.css_first("li").text(strip=True) == "no results".title()
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,status_code",
    [
        (
            {
                "term": "حم",
                "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "name",
            },
            404,
        ),
        (
            {
                "term": "حم",
                "app_label": "areas",
                "object_name": "governorate",
                "field_name": "name",
            },
            404,
        ),
        (
            {
                "term": "حم",
                "app_label": "areas",
                "model_name": "Governorate",
                "object_name": "governorate",
            },
            404,
        ),
        (
            {
                "term": "حم",
                "app_label": "areas",
                "model_name": "Governorate",
                "field_name": "name",
            },
            404,
        ),
        (
            {
                "term": "حم",
                "app_label": "areas",
                "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "namexx",
            },
            400,
        ),
        (
            {
                "term": "حم",
                "app_label": "areasx",
                "model_name": "Governorate",
                "object_name": "governorate",
                "field_name": "name",
            },
            404,
        ),
        (
            {
                "term": "حم",
                "app_label": "areas",
                "model_name": "Governoratef",
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
