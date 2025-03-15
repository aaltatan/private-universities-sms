import pytest
from django.test import Client
from rest_framework import status
from selectolax.parser import HTMLParser

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_delete_cities_page(
    admin_client: Client, model: type[Model], city_model: type[Model]
):
    obj = model.objects.first()

    for idx in range(3):
        city_model.objects.create(
            name=f"City xxxx-{idx}",
            governorate=obj,
            kind="city",
        )

    response = admin_client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    cities_table = parser.css_first("#cities-formset-table")
    rows = cities_table.css("table tbody[x-sort] tr")

    assert cities_table is not None
    assert len(rows) == 4
    assert city_model.objects.count() == 3

    response = admin_client.post(
        obj.get_update_url(),
        {
            "name": "Hama Governorate",
            "description": "some description",
            "cities-TOTAL_FORMS": 3,
            "cities-INITIAL_FORMS": 3,
            "cities-MIN_NUM_FORMS": 0,
            "cities-MAX_NUM_FORMS": 1000,
            "cities-0-id": 1,
            "cities-0-ORDER": 1,
            "cities-0-name": "City xxxx-0",
            "cities-0-kind": "city",
            "cities-0-description": "",
            "cities-1-id": 2,
            "cities-1-ORDER": 2,
            "cities-1-name": "City xxxx-1",
            "cities-1-kind": "city",
            "cities-1-description": "",
            "cities-2-id": 3,
            "cities-2-ORDER": 3,
            "cities-2-name": "City xxxx-2",
            "cities-2-kind": "city",
            "cities-2-description": "",
            "cities-2-DELETE": True,
            "update": "true",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert city_model.objects.count() == 2


@pytest.mark.django_db
def test_delete_cities_without_delete_perm_page(
    client: Client, model: type[Model], city_model: type[Model]
):
    client.login(
        username="city_user_with_change_add_perm",  # has no delete perm
        password="password",
    )

    obj = model.objects.first()

    for idx in range(3):
        city_model.objects.create(
            name=f"City xxxx-{idx}",
            governorate=obj,
            kind="city",
        )

    response = client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    cities_table = parser.css_first("#cities-formset-table")
    rows = cities_table.css("table tbody[x-sort] tr")

    assert cities_table is not None
    assert len(rows) == 4
    assert city_model.objects.count() == 3

    response = client.post(
        obj.get_update_url(),
        {
            "name": "Hama Governorate",
            "description": "some description",
            "cities-TOTAL_FORMS": 3,
            "cities-INITIAL_FORMS": 3,
            "cities-MIN_NUM_FORMS": 0,
            "cities-MAX_NUM_FORMS": 1000,
            "cities-0-id": 1,
            "cities-0-ORDER": 1,
            "cities-0-name": "City xxxx-0",
            "cities-0-kind": "city",
            "cities-0-description": "",
            "cities-1-id": 2,
            "cities-1-ORDER": 2,
            "cities-1-name": "City xxxx-1",
            "cities-1-kind": "city",
            "cities-1-description": "",
            "cities-2-id": 3,
            "cities-2-ORDER": 3,
            "cities-2-name": "City xxxx-2",
            "cities-2-kind": "city",
            "cities-2-description": "",
            "cities-2-DELETE": True,
            "update": "true",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert city_model.objects.count() == 3


@pytest.mark.django_db
def test_create_cities_page(
    admin_client: Client, model: type[Model], city_model: type[Model]
):
    obj = model.objects.first()

    for idx in range(3):
        city_model.objects.create(
            name=f"City xxxx-{idx}",
            governorate=obj,
            kind="city",
        )

    response = admin_client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    cities_table = parser.css_first("#cities-formset-table")
    rows = cities_table.css("table tbody[x-sort] tr")

    assert cities_table is not None
    assert len(rows) == 4
    assert city_model.objects.count() == 3

    response = admin_client.post(
        obj.get_update_url(),
        {
            "name": "Hama Governorate",
            "description": "some description",
            "cities-TOTAL_FORMS": 4,
            "cities-INITIAL_FORMS": 3,
            "cities-MIN_NUM_FORMS": 0,
            "cities-MAX_NUM_FORMS": 1000,
            "cities-0-id": 1,
            "cities-0-ORDER": 1,
            "cities-0-name": "City xxxx-0",
            "cities-0-kind": "city",
            "cities-0-description": "",
            "cities-1-id": 2,
            "cities-1-ORDER": 2,
            "cities-1-name": "City xxxx-1",
            "cities-1-kind": "city",
            "cities-1-description": "",
            "cities-2-id": 3,
            "cities-2-ORDER": 3,
            "cities-2-name": "City xxxx-2",
            "cities-2-kind": "city",
            "cities-2-description": "",
            "cities-3-id": "",
            "cities-3-ORDER": "",
            "cities-3-name": "City xxxx-3",
            "cities-3-kind": "city",
            "cities-3-description": "",
            "update": "true",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert city_model.objects.count() == 4


@pytest.mark.django_db
def test_create_cities_without_editing_total_forms(
    admin_client: Client, model: type[Model], city_model: type[Model]
):
    obj = model.objects.first()

    for idx in range(3):
        city_model.objects.create(
            name=f"City xxxx-{idx}",
            governorate=obj,
            kind="city",
        )

    response = admin_client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    cities_table = parser.css_first("#cities-formset-table")
    rows = cities_table.css("table tbody[x-sort] tr")

    assert cities_table is not None
    assert len(rows) == 4
    assert city_model.objects.count() == 3

    response = admin_client.post(
        obj.get_update_url(),
        {
            "name": "Hama Governorate",
            "description": "some description",
            "cities-TOTAL_FORMS": 3,  # must be 4 to create the new one
            "cities-INITIAL_FORMS": 3,
            "cities-MIN_NUM_FORMS": 0,
            "cities-MAX_NUM_FORMS": 1000,
            "cities-0-id": 1,
            "cities-0-ORDER": 1,
            "cities-0-name": "City xxxx-0",
            "cities-0-kind": "city",
            "cities-0-description": "",
            "cities-1-id": 2,
            "cities-1-ORDER": 2,
            "cities-1-name": "City xxxx-1",
            "cities-1-kind": "city",
            "cities-1-description": "",
            "cities-2-id": 3,
            "cities-2-ORDER": 3,
            "cities-2-name": "City xxxx-2",
            "cities-2-kind": "city",
            "cities-2-description": "",
            "cities-3-id": "",
            "cities-3-ORDER": "",
            "cities-3-name": "City xxxx-3",
            "cities-3-kind": "city",
            "cities-3-description": "",
            "update": "true",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert city_model.objects.count() == 3


@pytest.mark.django_db
def test_create_cities_without_create_perm(
    client: Client, model: type[Model], city_model: type[Model]
):
    client.login(
        username="city_user_with_change_perm",  # has no create perm
        password="password",
    )
    obj = model.objects.first()

    for idx in range(3):
        city_model.objects.create(
            name=f"City xxxx-{idx}",
            governorate=obj,
            kind="city",
        )

    response = client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    cities_table = parser.css_first("#cities-formset-table")
    rows = cities_table.css("table tbody[x-sort] tr")

    assert cities_table is not None
    assert len(rows) == 3
    assert city_model.objects.count() == 3

    response = client.post(
        obj.get_update_url(),
        {
            "name": "Hama Governorate",
            "description": "some description",
            "cities-TOTAL_FORMS": 4,
            "cities-INITIAL_FORMS": 3,
            "cities-MIN_NUM_FORMS": 0,
            "cities-MAX_NUM_FORMS": 1000,
            "cities-0-id": 1,
            "cities-0-ORDER": 1,
            "cities-0-name": "City xxxx-0",
            "cities-0-kind": "city",
            "cities-0-description": "",
            "cities-1-id": 2,
            "cities-1-ORDER": 2,
            "cities-1-name": "City xxxx-1",
            "cities-1-kind": "city",
            "cities-1-description": "",
            "cities-2-id": 3,
            "cities-2-ORDER": 3,
            "cities-2-name": "City xxxx-2",
            "cities-2-kind": "city",
            "cities-2-description": "",
            "cities-3-id": "",
            "cities-3-ORDER": "",
            "cities-3-name": "City xxxx-3",
            "cities-3-kind": "city",
            "cities-3-description": "",
            "update": "true",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert city_model.objects.count() == 3


@pytest.mark.django_db
def test_create_cities_without_create_perm_with_wrong_initial_forms(
    client: Client, model: type[Model], city_model: type[Model]
):
    client.login(
        username="city_user_with_change_perm",  # has no create perm
        password="password",
    )
    obj = model.objects.first()

    for idx in range(3):
        city_model.objects.create(
            name=f"City xxxx-{idx}",
            governorate=obj,
            kind="city",
        )

    response = client.get(obj.get_update_url())
    parser = HTMLParser(response.content)

    cities_table = parser.css_first("#cities-formset-table")
    rows = cities_table.css("table tbody[x-sort] tr")

    assert cities_table is not None
    assert len(rows) == 3
    assert city_model.objects.count() == 3

    response = client.post(
        obj.get_update_url(),
        {
            "name": "Hama Governorate",
            "description": "some description",
            "cities-TOTAL_FORMS": 4,
            "cities-INITIAL_FORMS": 4,
            "cities-MIN_NUM_FORMS": 0,
            "cities-MAX_NUM_FORMS": 1000,
            "cities-0-id": 1,
            "cities-0-ORDER": 1,
            "cities-0-name": "City xxxx-0",
            "cities-0-kind": "city",
            "cities-0-description": "",
            "cities-1-id": 2,
            "cities-1-ORDER": 2,
            "cities-1-name": "City xxxx-1",
            "cities-1-kind": "city",
            "cities-1-description": "",
            "cities-2-id": 3,
            "cities-2-ORDER": 3,
            "cities-2-name": "City xxxx-2",
            "cities-2-kind": "city",
            "cities-2-description": "",
            "cities-3-id": "",
            "cities-3-ORDER": "",
            "cities-3-name": "City xxxx-3",
            "cities-3-kind": "city",
            "cities-3-description": "",
            "update": "true",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert city_model.objects.count() == 3
