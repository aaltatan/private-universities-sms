import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from apps.core.models import AbstractUniqueNameModel as Model


@pytest.mark.django_db
def test_length_of_the_queryset(model: type[Model], counts: dict[str, int]):
    assert model.objects.count() == counts["objects"]


@pytest.mark.django_db
def test_unique_name_constraint(model: type[Model]):
    obj = model.objects.first()
    with pytest.raises(IntegrityError, match="UNIQUE constraint failed"):
        new_obj = model(
            name=obj.name,
            job_type=obj.job_type,
            description=obj.description,
        )
        new_obj.save()


@pytest.mark.django_db
def test_validators(
    model: type[Model],
    job_type_model: type[Model],
    models_dirty_data_test_cases: tuple[str],
):
    name, job_type_pk, description = models_dirty_data_test_cases
    job_type = job_type_model.objects.filter(pk=job_type_pk).first()
    with pytest.raises((ValidationError, IntegrityError)):
        obj = model.objects.create(
            name=name,
            job_type=job_type,
            description=description,
        )
        obj.full_clean()
