import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterSearchMixin,
    FilterTextMixin,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import nationalities as constants


class BaseNationalityFilter(FilterTextMixin, filters.FilterSet):
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())
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
