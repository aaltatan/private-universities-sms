import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model], counts: dict[str, int]):
    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_one_obj_has_local_nationality(model: type[Model]):
    assert model.objects.filter(is_local=True).count() == 1


@pytest.mark.django_db
def test_when_saving_new_object_then_all_qs_is_foreign(model: type[Model]):
    local_qs = model.objects.filter(is_local=True)

    assert local_qs.count() == 1

    local_obj = local_qs.first()
    model.objects.create(name="new dasdasd", is_local=True)

    local_qs = model.objects.filter(is_local=True)

    assert local_qs.count() == 1

    assert local_qs.first().name != local_obj.name



@pytest.mark.django_db
def test_validators(
    model: type[Model],
    models_dirty_data_test_cases: tuple[str, bool, str],
    counts: dict[str, int],
):
    name, is_local, description = models_dirty_data_test_cases
    count = model.objects.count()

    with pytest.raises((ValidationError, IntegrityError)):
        obj = model.objects.create(
            name=name,
            is_local=is_local,
            description=description,
        )
        obj.full_clean()

    assert count == counts["objects"]
