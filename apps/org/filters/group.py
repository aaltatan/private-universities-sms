from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BaseGroupFilter(BaseNameDescriptionFilter):
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Group
        fields = (
            "name",
            "kind",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APIGroupFilter(BaseGroupFilter):
    pass


class GroupFilter(BaseGroupFilter):
    pass
