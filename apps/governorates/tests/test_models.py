import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_name_field(model: type[Model]):
    object = model.objects.filter(name__contains="حماه").first()
    assert object.name == "محافظة حماه"
    assert object.slug == "محافظة-حماه"

    object = model.objects.filter(name__contains="حمص").first()
    assert object.name == "محافظة حمص"
    assert object.slug == "محافظة-حمص"

    object = model.objects.filter(name__contains="ادلب").first()
    assert object.name == "محافظة ادلب"
    assert object.slug == "محافظة-ادلب"

    object = model.objects.filter(name__contains="المنيا").first()
    assert object.name == "محافظة المنيا"
    assert object.slug == "محافظة-المنيا"


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model]):
    assert model.objects.count() == 4


@pytest.mark.django_db
def test_unique_name(model: type[Model]):
    with pytest.raises(IntegrityError):
        model.objects.create(name="محافظة حماه", description="حماه")


@pytest.mark.django_db
def test_less_than_four_characters(model: type[Model]):
    with pytest.raises(ValidationError):
        obj = model.objects.create(name="ddd", description="حماه")
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
