import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterComboboxMixin,
    FilterSearchMixin,
    FilterTextMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
)

from .. import models
from ..constants import job_subtypes


class BaseJobSubtypeFilter(FilterTextMixin, filters.FilterSet):
    name = filters.CharFilter(
        label=_("name").title(),
        method="filter_text",
    )
    description = filters.CharFilter(
        label=_("description").title(),
        method="filter_text",
    )

    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")


class APIJobSubtypeFilter(FilterComboboxMixin, BaseJobSubtypeFilter):
    job_type = get_combobox_choices_filter(
        model=models.JobSubtype,
        field_name="job_type__name",
        label=_("job type"),
        api_filter=True,
    )


class JobSubtypeFilter(
    FilterComboboxMixin,
    FilterSearchMixin,
    BaseJobSubtypeFilter,
):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(job_subtypes.ORDERING_FIELDS)
    job_type = get_combobox_choices_filter(
        model=models.JobSubtype,
        field_name="job_type__name",
        label=_("job type"),
    )