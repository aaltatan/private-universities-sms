import django_filters as filters
from django.utils.translation import gettext as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_number_from_to_filters,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import positions as constants


class BasePositionFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())
    order_from, order_to = get_number_from_to_filters(field_name="order")

    class Meta:
        model = models.Position
        fields = ("name", "order_from", "order_to", "description")


class APIPositionFilter(BasePositionFilter):
    pass


class PositionFilter(FilterSearchMixin, BasePositionFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
