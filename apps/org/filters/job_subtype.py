from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
)

from .. import models
from ..constants import job_subtypes as constants


class BaseJobSubtypeFilter(BaseNameDescriptionFilter):
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
    BaseQSearchFilter,
    BaseJobSubtypeFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    job_type = get_combobox_choices_filter(
        model=models.JobSubtype,
        field_name="job_type__name",
        label=_("job type"),
    )
