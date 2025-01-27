import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterSearchMixin, get_order_by_filter
from apps.core.widgets import ComboboxWidget

from . import constants, models


class CityFilter(
    filters.FilterSet,
    FilterSearchMixin,
):
    q = filters.CharFilter(method="search")
    order_by = get_order_by_filter(constants.ORDERING_FIELDS)
    name = filters.CharFilter(
        lookup_expr="icontains",
        label=_("name").title(),
    )
    governorate = filters.ModelMultipleChoiceFilter(
        queryset=models.Governorate.objects.all(),
        label=_("governorate").title(),
        widget=ComboboxWidget({"data-name": "governorates"}),
    )
    description = filters.CharFilter(
        lookup_expr="icontains",
        label=_("description").title(),
    )

    class Meta:
        model = models.City
        fields = ("name", "governorate", "description")
