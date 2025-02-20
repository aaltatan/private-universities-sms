import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model], counts: dict[str, int]):
    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_validators(
    model: type[Model],
    models_dirty_data_test_cases: tuple[str, bool, str],
    counts: dict[str, int],
):
    name, is_payable, description = models_dirty_data_test_cases
    count = model.objects.count()

    with pytest.raises((ValidationError, IntegrityError)):
        obj = model.objects.create(
            name=name,
            is_payable=is_payable,
            description=description,
        )
        obj.full_clean()

    assert count == counts["objects"]
