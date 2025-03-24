from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_number_from_to_filters,
)

from .. import models


class BaseCitiesFilter(BaseNameDescriptionFilter):
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.City
        fields = (
            "name",
            "governorate",
            "employees_count_from",
            "employees_count_to",
            "kind",
            "description",
        )


class APICitiesFilter(FilterComboboxMixin, BaseCitiesFilter):
    governorate = get_combobox_choices_filter(
        model=models.City,
        field_name="governorate__name",
        label=_("governorate"),
        api_filter=True,
    )


class CityFilter(FilterComboboxMixin, BaseCitiesFilter):
    governorate = get_combobox_choices_filter(
        model=models.City,
        field_name="governorate__name",
        label=_("governorate"),
    )
