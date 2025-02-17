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
from ..constants import cities as constants


class BaseCitiesFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())

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


class CityFilter(FilterComboboxMixin, FilterSearchMixin, BaseCitiesFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    governorate = get_combobox_choices_filter(
        model=models.City,
        field_name="governorate__name",
        label=_("governorate"),
    )
