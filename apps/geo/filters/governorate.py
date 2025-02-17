from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
)

from .. import models
from ..constants import governorates as constants


class BaseGovernoratesFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")


class APIGovernoratesFilter(BaseGovernoratesFilter):
    pass


class GovernorateFilter(BaseQSearchFilter, BaseGovernoratesFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
