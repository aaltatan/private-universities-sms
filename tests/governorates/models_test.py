import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_name_field(model: type[Model], models_data_test_cases: tuple[str]):
    filter_, name, _, slug = models_data_test_cases
    object = model.objects.filter(name__contains=filter_).first()
    assert object.name == name
    assert object.slug == slug


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model]):
    assert model.objects.count() == 304


@pytest.mark.django_db
def test_unique_name_constraint(
    model: type[Model],
    models_data_test_cases: tuple[str, ...],
):
    _, name, description, _ = models_data_test_cases
    with pytest.raises(IntegrityError):
        model.objects.create(name=name, description=description)


@pytest.mark.django_db
def test_validators(
    model: type[Model],
    models_dirty_data_test_cases: tuple[str],
):
    name, description = models_dirty_data_test_cases
    with pytest.raises(ValidationError):
        obj = model.objects.create(name=name, description=description)
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
