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
    nationality_model: type[Model],
    school_kind_model: type[Model],
):
    (
        name,
        nationality_id,
        kind_id,
        website,
        email,
        phone,
        description,
    ) = models_dirty_data_test_cases

    nationality = nationality_model.objects.get(id=nationality_id)
    kind = school_kind_model.objects.get(id=kind_id)

    with pytest.raises(ValidationError):
        obj = model.objects.create(
            name=name,
            nationality=nationality,
            kind=kind,
            website=website,
            email=email,
            phone=phone,
            description=description,
        )
        obj.full_clean()
