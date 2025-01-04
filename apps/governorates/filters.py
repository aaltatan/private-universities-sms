import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterSearchMixin, get_order_by_filter

from . import models


class GovernorateFilter(
    filters.FilterSet,
    FilterSearchMixin,
):
    q = filters.CharFilter(method="search")
    order_by = get_order_by_filter(
        {
            "id": _("id").title(),
            "name": _("name").title(),
            "description": _("description").title(),
        }
    )
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
