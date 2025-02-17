from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
)

from .. import models
from ..constants import job_types as constants


class BaseJobTypeFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.JobType
        fields = ("name", "description")


class APIJobTypeFilter(BaseJobTypeFilter):
    pass


class JobTypeFilter(BaseQSearchFilter, BaseJobTypeFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
