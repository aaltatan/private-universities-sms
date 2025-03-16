from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_number_from_to_filters,
    get_ordering_filter,
)

from .. import models
from ..constants import groups as constants


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


class GroupFilter(BaseQSearchFilter, BaseGroupFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
