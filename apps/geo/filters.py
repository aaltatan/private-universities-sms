import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterComboboxMixin,
    FilterSearchMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
)

from . import models
from .constants import cities, governorates, nationalities


class BaseGovernoratesFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        label=_("name").title(),
    )
    description = filters.CharFilter(
        lookup_expr="icontains",
        label=_("description").title(),
    )

    class Meta:
        model = models.Governorate
        fields = ("name", "description")


class APIGovernoratesFilter(BaseGovernoratesFilter):
    pass


class GovernorateFilter(FilterSearchMixin, BaseGovernoratesFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(governorates.ORDERING_FIELDS)


class BaseCitiesFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        label=_("name").title(),
    )
    description = filters.CharFilter(
        lookup_expr="icontains",
        label=_("description").title(),
    )

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
    ordering = get_ordering_filter(cities.ORDERING_FIELDS)
    governorate = get_combobox_choices_filter(
        model=models.City,
        field_name="governorate__name",
        label=_("governorate"),
    )


class BaseNationalityFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        label=_("name").title(),
    )
    is_local = filters.ChoiceFilter(
        label=_("locality").title(),
        choices=models.Nationality.IS_LOCAL_CHOICES,
    )
    description = filters.CharFilter(
        lookup_expr="icontains",
        label=_("description").title(),
    )

    class Meta:
        model = models.Nationality
        fields = ("name", "is_local", "description")


class APINationalityFilter(BaseNationalityFilter):
    pass


class NationalityFilter(FilterSearchMixin, BaseNationalityFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(nationalities.ORDERING_FIELDS)
