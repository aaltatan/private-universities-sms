import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
)

from .. import models
from ..constants import nationalities as constants


class BaseNationalityFilter(FilterTextMixin, filters.FilterSet):
    name = filters.CharFilter(
        label=_("name").title(),
        method="filter_text",
    )
    description = filters.CharFilter(
        label=_("description").title(),
        method="filter_text",
    )
    is_local = filters.ChoiceFilter(
        label=_("locality").title(),
        choices=models.Nationality.IS_LOCAL_CHOICES,
    )

    class Meta:
        model = models.Nationality
        fields = ("name", "is_local", "description")


class APINationalityFilter(BaseNationalityFilter):
    pass


class NationalityFilter(FilterSearchMixin, BaseNationalityFilter):
    q = filters.CharFilter(method="search")
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
