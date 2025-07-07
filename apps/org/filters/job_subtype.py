from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_number_from_to_filters,
)

from .. import models


class BaseJobSubtypeFilter(BaseNameDescriptionFilter):
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.JobSubtype
        fields = (
            "name",
            "job_type",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APIJobSubtypeFilter(FilterComboboxMixin, BaseJobSubtypeFilter):
    job_type = get_combobox_choices_filter(
        queryset=models.JobSubtype.objects.all(),
        field_name="job_type__name",
        label=_("job type"),
        api_filter=True,
    )


class JobSubtypeFilter(FilterComboboxMixin, BaseJobSubtypeFilter):
    job_type = get_combobox_choices_filter(
        queryset=models.JobSubtype.objects.all(),
        field_name="job_type__name",
        label=_("job type"),
    )
