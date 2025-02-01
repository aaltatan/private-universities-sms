import pytest
import pytest_mock
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_pagination(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response = api_client.get(
        path=urls["api"],
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 304
    assert len(response.json()["results"]) == 10
    assert response.json()["next"].endswith(urls["api"] + "?page=2")
    assert response.json()["previous"] is None

    response = api_client.get(
        path=urls["api"] + "?page=2",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 304
    assert len(response.json()["results"]) == 10
    assert response.json()["next"].endswith(urls["api"] + "?page=3")
    assert response.json()["previous"].endswith(urls["api"])

    response = api_client.get(
        path=urls["api"] + "?page=31",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 304
    assert len(response.json()["results"]) == 4
    assert response.json()["next"] is None
    assert response.json()["previous"].endswith(urls["api"] + "?page=30")

    for idx in range(3, 31):
        response = api_client.get(
            path=urls["api"] + f"?page={idx}",
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 304
        assert len(response.json()["results"]) == 10
        assert response.json()["next"].endswith(urls["api"] + f"?page={idx + 1}")
        assert response.json()["previous"].endswith(urls["api"] + f"?page={idx - 1}")


@pytest.mark.django_db
def test_read_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=urls["api"],
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 304
    assert len(response.json()["results"]) == 10


@pytest.mark.django_db
def test_filter_objects_using_q(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f"{urls['api']}?q=City+40",
        headers=admin_headers,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 3  # 40, 140, 240,


@pytest.mark.django_db
def test_filter_objects_using_djangoql(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f"{urls['api']}?q=id<4",
        headers=admin_headers,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert {
        "id": 1,
        "name": "محافظة حماه",
        "description": "goo",
        "slug": "محافظة-حماه",
    } in response.json()["results"]

    assert response.json()["count"] == 3


@pytest.mark.django_db
def test_filter_objects_using_djangoql_endswith(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f'{urls["api"]}?q=name endswith "3"',
        headers=admin_headers,
        format="json",
    )
    ids = [i for i in range(1, 301) if str(i).endswith("3")]

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == len(ids)


@pytest.mark.django_db
def test_delete_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    model_name: str,
):
    for idx in range(1, 11):
        response: Response = api_client.delete(
            path=f"{urls['api']}{idx}/",
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert model.objects.count() == 294

    response: Response = api_client.get(
        path=f"{urls['api']}312312",
        headers=admin_headers,
        follow=True,
    )
    assert response.json() == {"detail": f"No {model_name} matches the given query."}
    assert response.status_code == 404
    assert model.objects.count() == 294


@pytest.mark.django_db
def test_delete_and_bulk_delete_object_when_deleter_class_is_None(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(f"apps.{app_label}.views.APIViewSet.deleter", new=None)

    with pytest.raises(AttributeError):
        api_client.delete(
            path=f"{urls['api']}1/",
            headers=admin_headers,
        )

    with pytest.raises(AttributeError):
        api_client.post(
            path=f"{urls['api']}bulk-delete/",
            data={"ids": [1, 2, 3, 4, 500, 501]},
            headers=admin_headers,
        )


@pytest.mark.django_db
def test_delete_and_bulk_delete_object_when_deleter_class_is_not_a_subclass_of_Deleter(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    class Deleter: ...

    mocker.patch(f"apps.{app_label}.views.APIViewSet.deleter", new=Deleter)

    with pytest.raises(TypeError):
        api_client.delete(
            path=f"{urls['api']}1/",
            headers=admin_headers,
        )

    with pytest.raises(TypeError):
        api_client.post(
            path=f"{urls['api']}bulk-delete/",
            data={"ids": [1, 2, 3, 4, 500, 501]},
            headers=admin_headers,
        )


@pytest.mark.django_db
def test_delete_object_undeletable(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    model_name: str,
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(
        f"apps.{app_label}.utils.Deleter.is_obj_deletable",
        return_value=False,
    )

    for idx in range(1, 11):
        response: Response = api_client.delete(
            path=f"{urls['api']}{idx}/",
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["details"].endswith("cannot be deleted.")

    assert model.objects.count() == 304

    response: Response = api_client.get(
        path=f"{urls['api']}312312",
        headers=admin_headers,
        follow=True,
    )
    assert response.json() == {"detail": f"No {model_name} matches the given query."}
    assert response.status_code == 404
    assert model.objects.count() == 304


@pytest.mark.django_db
def test_bulk_delete_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [1, 2, 3, 4, 500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert model.objects.count() == 300

    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert model.objects.count() == 300


@pytest.mark.django_db
def test_bulk_delete_objects_undeletable(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
):
    mocker.patch(
        f"apps.{app_label}.utils.Deleter.is_qs_deletable",
        return_value=False,
    )

    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [1, 2, 3, 4, 500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["details"] == "selected 4 objects cannot be deleted."
    assert model.objects.count() == 304

    response: Response = api_client.post(
        path=f"{urls['api']}bulk-delete/",
        data={"ids": [500, 501]},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert model.objects.count() == 304


@pytest.mark.django_db
def test_read_objects_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=urls["api"],
        headers=user_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_read_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    response: Response = api_client.get(
        path=f"{urls['api']}{model.objects.get(id=1).pk}/",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "محافظة حماه"


@pytest.mark.django_db
def test_read_object_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f"{urls['api']}1/",
        headers=user_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_read_object_with_invalid_id(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
):
    response: Response = api_client.get(
        path=f"{urls['api']}4123/",
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    response: Response = api_client.put(
        path=f"{urls['api']}1/",
        data={
            "name": "Hamah",
            "description": "some description",
        },
        headers=admin_headers,
        follow=True,
    )
    first = model.objects.get(id=1)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Hamah"
    assert response.json()["description"] == "some description"
    assert first.name == "Hamah"
    assert first.description == "some description"


@pytest.mark.django_db
def test_update_object_with_dirty_data(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    dirty_data: list[dict],
):
    for data in dirty_data:
        response: Response = api_client.put(
            path=f"{urls['api']}3/",
            data=data["data"],
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["name"] == data["api_error"]


@pytest.mark.django_db
def test_create_objects(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    for idx in range(500, 550):
        response = api_client.post(
            path=urls["api"],
            data={"name": f"City {idx}"},
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == f"City {idx}"

    response: Response = api_client.get(
        path=urls["api"],
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 354
    assert model.objects.count() == 354


@pytest.mark.django_db
def test_create_object_without_permissions(
    api_client: APIClient,
    urls: dict[str, str],
    user_headers: dict[str, str],
):
    response = api_client.post(
        path=urls["api"],
        data={"name": "City"},
        headers=user_headers,
    )
    assert response.status_code == 403

    response: Response = api_client.post(
        path=urls["api"],
        data={"name": "City"},
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_object_with_dirty_data(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    dirty_data: list[dict],
):
    for data in dirty_data:
        response: Response = api_client.post(
            path=urls["api"],
            data=data["data"],
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["name"] == data["api_error"]
