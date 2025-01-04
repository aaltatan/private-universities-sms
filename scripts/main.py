from django.db.models import Window, F
from django.db.models.functions import DenseRank

from apps.governorates.models import Governorate


def run():
    field = "-name"
    descending = field.startswith("-")
    field_name = field[1:] if descending else field

    print(field_name)

    order_by_window_field = F(field_name).asc() if descending else F(field_name).desc()

    qs = Governorate.objects.order_by(field).annotate(
        index=Window(
            expression=DenseRank(),
            order_by=order_by_window_field,
        )
    )
    for obj in qs:
        print(f"{obj.name=}")
        print(f"{obj.index=}")
