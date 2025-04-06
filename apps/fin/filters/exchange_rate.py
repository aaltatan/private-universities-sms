import django_filters as filters
from django.utils.translation import gettext as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    get_date_from_to_filters,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseExchangeRateFilter(BaseNameDescriptionFilter):
    created_at_from, created_at_to = get_date_from_to_filters("created_at")
    updated_at_from, updated_at_to = get_date_from_to_filters("updated_at")
    date_from, date_to = get_date_from_to_filters("date")
    rate_from, rate_to = get_number_from_to_filters("rate")
    notes = get_text_filter(label=_("notes").title())
    is_primary = filters.ChoiceFilter(
        field_name="currency__is_primary",
        choices=models.Currency.IsPrimaryChoices.choices,
        label=_("is primary"),
    )

    class Meta:
        model = models.ExchangeRate
        fields = (
            "currency",
            "is_primary",
            "created_at_from",
            "created_at_to",
            "updated_at_from",
            "updated_at_to",
            "date_from",
            "date_to",
            "rate_from",
            "rate_to",
            "notes",
        )


class APIExchangeRateFilter(BaseExchangeRateFilter):
    pass


class ExchangeRateFilter(BaseExchangeRateFilter):
    pass
