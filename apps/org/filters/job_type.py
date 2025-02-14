import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
)

from .. import models
from ..constants import job_types


class BaseJobTypeFilter(FilterTextMixin, filters.FilterSet):
    name = filters.CharFilter(
        label=_("name").title(),
        method="filter_text",
    )
    description = filters.CharFilter(
        label=_("description").title(),
        method="filter_text",
    )

    class Meta:
        model = models.JobType
        fields = ("name", "description")


class APIJobTypeFilter(BaseJobTypeFilter):
    pass


class JobTypeFilter(FilterSearchMixin, BaseJobTypeFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(job_types.ORDERING_FIELDS)
