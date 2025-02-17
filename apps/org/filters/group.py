import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import groups as constants


class BaseGroupFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())

    class Meta:
        model = models.Group
        fields = ("name", "description")


class APIGroupFilter(BaseGroupFilter):
    pass


class GroupFilter(FilterSearchMixin, BaseGroupFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
