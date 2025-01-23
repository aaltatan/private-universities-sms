import pytest
from django.test import Client
from selectolax.parser import HTMLParser

from tests.utils import is_template_used


@pytest.mark.django_db
def test_autocomplete_without_permissions(
    client: Client,
    autocomplete_url: str,
    create_governorates,
) -> None:
    client.login(
        username="user_with_no_perm",
        password="user_with_no_perm",
    )
    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = client.get(autocomplete_url, payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_autocomplete(
    admin_client: Client,
    autocomplete_url: str,
    autocomplete_template: str,
    create_governorates,
):
    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")
    for li in lis:
        assert li.text(strip=True) in [
            "محافظة حماه",
            "محافظة حمص",
        ]

    assert is_template_used(autocomplete_template, response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_autocomplete_with_no_permissions(
    admin_client: Client,
    autocomplete_url: str,
    autocomplete_template: str,
    create_governorates,
):
    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")
    for li in lis:
        assert li.text(strip=True) in [
            "محافظة حماه",
            "محافظة حمص",
        ]

    assert is_template_used(autocomplete_template, response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_autocomplete_with_empty_term(
    admin_client: Client,
    autocomplete_url: str,
    autocomplete_template: str,
    create_governorates,
):
    payload = {
        "term": "xx",
        "app_label": "governorates",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)
    parser = HTMLParser(response.content)

    lis = parser.css("li")

    assert len(lis) == 1
    assert is_template_used(autocomplete_template, response)
    assert parser.css_first("li").text(strip=True) == "no results".title()
    assert response.status_code == 200


@pytest.mark.django_db
def test_autocomplete_with_dirty_payload(
    admin_client: Client,
    autocomplete_url: str,
    autocomplete_template: str,
):
    payload = {
        "term": "حم",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 404

    payload = {
        "term": "حم",
        "app_label": "governorates",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 404

    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governorate",
        "object_name": "governorate",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 404

    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 404

    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "namexx",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 400

    payload = {
        "term": "حم",
        "app_label": "governoratesx",
        "model_name": "Governorate",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 404

    payload = {
        "term": "حم",
        "app_label": "governorates",
        "model_name": "Governoratef",
        "object_name": "governorate",
        "field_name": "name",
    }
    response = admin_client.get(autocomplete_url, payload)

    assert response.status_code == 404
