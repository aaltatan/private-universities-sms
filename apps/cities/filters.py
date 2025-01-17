import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterSearchMixin, get_order_by_filter

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
    description = filters.CharFilter(
        lookup_expr="icontains",
        label=_("description").title(),
    )

    class Meta:
        model = models.City
        fields = ("name", "description")
