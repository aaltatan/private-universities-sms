from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
    get_number_from_to_filters,
)

from .. import models
from ..constants import governorates as constants


class BaseGovernoratesFilter(BaseNameDescriptionFilter):
    cities_count_from, cities_count_to = get_number_from_to_filters("cities_count")
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Governorate
        fields = (
            "name",
            "cities_count_from",
            "cities_count_to",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APIGovernoratesFilter(BaseGovernoratesFilter):
    pass


class GovernorateFilter(BaseQSearchFilter, BaseGovernoratesFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
