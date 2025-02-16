import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
)

from .. import models
from ..constants import cost_centers as constants


class BaseCostCenterFilter(FilterTextMixin, filters.FilterSet):
    name = filters.CharFilter(
        label=_("name").title(),
        method="filter_text",
    )
    description = filters.CharFilter(
        label=_("description").title(),
        method="filter_text",
    )

    class Meta:
        model = models.CostCenter
        fields = ("name", "accounting_id", "description")


class APICostCenterFilter(BaseCostCenterFilter):
    pass


class CostCenterFilter(FilterSearchMixin, BaseCostCenterFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
