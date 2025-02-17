import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterComboboxMixin,
    FilterSearchMixin,
    FilterTextMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import job_subtypes as constants


class BaseJobSubtypeFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())

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
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    job_type = get_combobox_choices_filter(
        model=models.JobSubtype,
        field_name="job_type__name",
        label=_("job type"),
    )
