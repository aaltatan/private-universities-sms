import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model
from tests.utils import load_yaml


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["models"]["data"],
)
def test_name_field(model: type[Model], params: dict):
    object = model.objects.filter(name__contains=params["filter"]).first()
    assert object.name == params["name"]
    assert object.slug == params["slug"]


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model]):
    assert model.objects.count() == 304


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["models"]["data"],
)
def test_unique_name_constraint(model: type[Model], params: dict):
    with pytest.raises(IntegrityError):
        model.objects.create(
            name=params["name"],
            description=params["description"],
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    load_yaml("test_cases.yaml", "governorates")["models"]["dirty_data"],
)
def test_validators(model: type[Model], params: dict):
    with pytest.raises(ValidationError):
        obj = model.objects.create(
            name=params["name"],
            description=params["description"],
        )
        obj.full_clean()


@pytest.mark.django_db
def test_slug_signal(model: type[Model]):
    names = [
        "abcdefghijklmnopqrstuvwxyz",
        "Abcdefghijklmnopqrstuvwxyz",
        "ABcdefghijklmnopqrstuvwxyz",
        "AbCDefghijklmnopqrstuvwxyz",
        "ABCdEFgHIJKLMNOPQRSTUVWXYZ",
        "ABCdEFgHIJKLMNOPQRSTUVWxYZ",
        "ABCdEFgHIJKLMNOPQRSTUVWxyz",
        "ABCdEFgHIJKLMNOPqRSTUVWxyz",
        "ABCdEFgHIJKLMnOPqRSTUVWxyz",
        "ABCdEFgHIJKLmnOPqRSTUVWxyz",
        "ABCdEFgHIJKLmnOPqRSTUVwxyz",
        "ABCdEFgHIJKLmnOPqRSTUvwxyz",
        "ABCdEFgHIJKLmnOPqRSTuvwxyz",
        "ABCdEFgHIJKLmnOPqRStuvwxyz",
        "ABCdEFgHIJKLmnOPqRstuvwxyz",
        "ABCdEFgHIJKLmnOPqrstuvwxyz",
        "ABCdEFgHIJKLmnOpqrstuvwxyz",
    ]
    names += [name.swapcase() for name in names]

    for idx, name in enumerate(names):
        obj = model.objects.create(
            name=name,
            description=name,
        )
        if idx == 0:
            assert obj.slug == "abcdefghijklmnopqrstuvwxyz"
        else:
            assert obj.slug == f"abcdefghijklmnopqrstuvwxyz{idx}"

    names = [
        "google is",
        "google-is",
        "google----is",
        "google       is",
        "google       is   ",
        "   google       is   ",
    ]
    names += [name.swapcase() for name in names]

    for idx, name in enumerate(names):
        obj = model.objects.create(name=name, description=name)
        if idx == 0:
            assert obj.slug == "google-is"
        else:
            assert obj.slug == f"google-is{idx}"
