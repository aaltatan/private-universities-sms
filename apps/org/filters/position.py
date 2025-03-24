from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BasePositionFilter(BaseNameDescriptionFilter):
    order_from, order_to = get_number_from_to_filters(field_name="order")
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Position
        fields = (
            "name",
            "order_from",
            "order_to",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APIPositionFilter(BasePositionFilter):
    pass


class PositionFilter(BasePositionFilter):
    pass
