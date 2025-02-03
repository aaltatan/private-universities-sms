import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterSearchMixin, get_ordering_filter

from . import constants, models


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
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
