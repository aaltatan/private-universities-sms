import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterSearchMixin, get_ordering_filter
from apps.core.widgets import ComboboxWidget

from . import constants, models


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


class APICitiesFilter(BaseCitiesFilter):
    governorate = filters.ModelMultipleChoiceFilter(
        queryset=models.Governorate.objects.all(),
        label=_("governorate").title(),
    )


class CityFilter(BaseCitiesFilter, FilterSearchMixin):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    governorate = filters.ModelMultipleChoiceFilter(
        queryset=models.Governorate.objects.all(),
        label=_("governorate").title(),
        widget=ComboboxWidget({"data-name": "governorates"}),
    )
