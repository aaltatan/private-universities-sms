import pytest

from django.forms import ValidationError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model], counts: dict[str, int]):
    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_validators(
    model: type[Model],
    models_dirty_data_test_cases: tuple[str],
):
    name, kind, description = models_dirty_data_test_cases
    with pytest.raises(ValidationError):
        obj = model.objects.create(name=name, description=description, kind=kind)
        obj.full_clean()
