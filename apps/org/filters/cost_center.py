import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import cost_centers as constants


class BaseCostCenterFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())
    accounting_id = get_text_filter(label=_("accounting id").title())

    class Meta:
        model = models.CostCenter
        fields = ("name", "accounting_id", "description")


class APICostCenterFilter(BaseCostCenterFilter):
    pass


class CostCenterFilter(FilterSearchMixin, BaseCostCenterFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
