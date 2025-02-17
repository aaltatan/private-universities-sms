import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import job_types as constants


class BaseJobTypeFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())

    class Meta:
        model = models.JobType
        fields = ("name", "description")


class APIJobTypeFilter(BaseJobTypeFilter):
    pass


class JobTypeFilter(FilterSearchMixin, BaseJobTypeFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
