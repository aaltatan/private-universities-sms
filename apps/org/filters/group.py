from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
)

from .. import models
from ..constants import groups as constants


class BaseGroupFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.Group
        fields = ("name", "kind", "description")


class APIGroupFilter(BaseGroupFilter):
    pass


class GroupFilter(BaseQSearchFilter, BaseGroupFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
