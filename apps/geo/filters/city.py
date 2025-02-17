from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
)

from .. import models
from ..constants import cities as constants


class BaseCitiesFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.City
        fields = ("name", "governorate", "description")


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
