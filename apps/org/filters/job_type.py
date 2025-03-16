from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
    get_number_from_to_filters,
)

from .. import models
from ..constants import job_types as constants


class BaseJobTypeFilter(BaseNameDescriptionFilter):
    job_subtypes_count_from, job_subtypes_count_to = get_number_from_to_filters(
        "job_subtypes_count"
    )
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.JobType
        fields = (
            "name",
            "job_subtypes_count_from",
            "job_subtypes_count_to",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APIJobTypeFilter(BaseJobTypeFilter):
    pass


class JobTypeFilter(BaseQSearchFilter, BaseJobTypeFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
