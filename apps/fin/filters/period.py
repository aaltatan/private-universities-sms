import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_date_from_to_filters,
)

from .. import models


class BasePeriodFilter(BaseNameDescriptionFilter):
    is_closed = filters.ChoiceFilter(
        label=_("closed"),
        choices=models.Period.ClosedChoices,
    )
    start_date_from, start_date_to = get_date_from_to_filters("start_date")

    class Meta:
        model = models.Period
        fields = (
            "name",
            "year",
            "start_date_from",
            "start_date_to",
            "is_closed",
            "description",
        )


class APIPeriodFilter(FilterComboboxMixin, BasePeriodFilter):
    pass


class PeriodFilter(FilterComboboxMixin, BasePeriodFilter):
    pass
