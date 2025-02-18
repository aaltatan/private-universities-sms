import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_name_field(model: type[Model], models_data_test_cases: tuple[str]):
    filter_, name, order, _, slug = models_data_test_cases
    object = model.objects.filter(name__contains=filter_).first()
    assert object.name == name
    assert object.order == order
    assert object.slug == slug


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model], counts: dict[str, int]):
    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_unique_name_constraint(
    model: type[Model],
    models_data_test_cases: tuple[str, ...],
):
    _, name, order, description, _ = models_data_test_cases
    with pytest.raises(IntegrityError):
        model.objects.create(name=name, order=order, description=description)


@pytest.mark.django_db
def test_validators(
    model: type[Model],
    models_dirty_data_test_cases: tuple[str],
):
    name, order, description = models_dirty_data_test_cases
    with pytest.raises(ValidationError):
        obj = model.objects.create(
            name=name,
            order=order,
            description=description,
        )
        obj.full_clean()
