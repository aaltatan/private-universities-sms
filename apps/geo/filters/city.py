from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_number_from_to_filters,
    get_ordering_filter,
)

from .. import models
from ..constants import cities as constants


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


class CityFilter(
    FilterComboboxMixin,
    BaseQSearchFilter,
    BaseCitiesFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    governorate = get_combobox_choices_filter(
        model=models.City,
        field_name="governorate__name",
        label=_("governorate"),
    )
