from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BaseGovernorateFilter(BaseNameDescriptionFilter):
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


class APIGovernorateFilter(BaseGovernorateFilter):
    pass


class GovernorateFilter(BaseGovernorateFilter):
    pass
