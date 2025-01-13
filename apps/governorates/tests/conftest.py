import pytest

from django.db.models import Model

from ..models import Governorate


@pytest.fixture
def model() -> type[Model]:
    return Governorate


@pytest.fixture(autouse=True)
def governorates() -> None:
    governorates = [
        {"name": "محافظة حماه", "description": "حماه"},
        {"name": "محافظة حمص", "description": "حمص"},
        {"name": "محافظة ادلب", "description": "ادلب"},
        {"name": "محافظة المنيا", "description": "المنيا"},
    ]
    for governorate in governorates:
        Governorate.objects.create(**governorate)
