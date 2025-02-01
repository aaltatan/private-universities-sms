import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter,expected_name,expected_slug",
    [
        ("حماه", "محافظة حماه", "محافظة-حماه"),
        ("حمص", "محافظة حمص", "محافظة-حمص"),
        ("ادلب", "محافظة ادلب", "محافظة-ادلب"),
        ("المنيا", "محافظة المنيا", "محافظة-المنيا"),
    ],
)
def test_name_field(
    model: type[Model],
    filter: str,
    expected_name: str,
    expected_slug: str,
):
    object = model.objects.filter(name__contains=filter).first()
    assert object.name == expected_name
    assert object.slug == expected_slug


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model]):
    assert model.objects.count() == 304


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name",
    [
        "محافظة حماه",
        "محافظة حمص",
        "محافظة ادلب",
        "محافظة المنيا",
    ],
)
def test_unique_name_constraint(model: type[Model], name: str):
    with pytest.raises(IntegrityError):
        model.objects.create(name=name, description="حماه")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name,description",
    [
        ("", "goo"),
        ("x", "meta"),
        ("xx", "meta"),
        ("xxx", "language mena"),
    ],
)
def test_validators(model: type[Model], name: str, description: str):
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
