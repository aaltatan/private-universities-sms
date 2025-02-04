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
    api_pagination_test_cases: tuple[str, int, str, str],
):
    query_string, count, next_page, prev_page = api_pagination_test_cases
    response: Response = api_client.get(
        path=urls["api"] + query_string,
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 304
    assert len(response.json()["results"]) == count

    if next_page is not None:
        assert response.json()["next"].endswith(urls["api"] + next_page)
    else:
        assert response.json()["next"] is None

    if prev_page is not None:
        assert response.json()["previous"].endswith(urls["api"] + prev_page)
    else:
        assert response.json()["previous"] is None


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
def test_delete_object(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
):
    for idx in range(1, 11):
        response: Response = api_client.delete(
            path=f"{urls['api']}{idx}/",
            headers=admin_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    assert model.objects.count() == 294


@pytest.mark.django_db
def test_delete_object_with_invalid_id(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    model_name: str,
):
    response: Response = api_client.get(
        path=f"{urls['api']}312312",
        headers=admin_headers,
        follow=True,
    )
    assert response.json() == {"detail": f"No {model_name} matches the given query."}
    assert response.status_code == 404
    assert model.objects.count() == 304


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
@pytest.mark.parametrize("idx", list(range(1, 11)))
def test_delete_object_undeletable(
    api_client: APIClient,
    urls: dict[str, str],
    admin_headers: dict[str, str],
    model: type[Model],
    mocker: pytest_mock.MockerFixture,
    app_label: str,
    idx: int,
):
    mocker.patch(
        f"apps.{app_label}.utils.Deleter.is_obj_deletable",
        return_value=False,
    )

    response: Response = api_client.delete(
        path=f"{urls['api']}{idx}/",
        headers=admin_headers,
    )

    assert model.objects.count() == 304
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["details"].endswith("cannot be deleted.")


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
    api_client: APIClient, urls: dict[str, str], user_headers: dict[str, str]
):
    response: Response = api_client.get(
        path=urls["api"],
        headers=user_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_read_object(
    api_client: APIClient, urls: dict[str, str], admin_headers: dict[str, str]
):
    response: Response = api_client.get(
        path=f"{urls['api']}1/",
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
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
):
    data, _, error = dirty_data_test_cases
    response: Response = api_client.put(
        path=f"{urls['api']}3/", data=data, headers=admin_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["name"] == error


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
        path=urls["api"], data={"name": "City"}, headers=user_headers
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
    dirty_data_test_cases: tuple[dict[str, str], str, list[str]],
):
    data, _, error = dirty_data_test_cases
    response: Response = api_client.post(
        path=urls["api"], data=data, headers=admin_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["name"] == error
