import django_filters as filters
from django.utils.translation import gettext as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseCurrencyFilter(BaseNameDescriptionFilter):
    decimal_places_from, decimal_places_to = get_number_from_to_filters(
        "decimal_places"
    )
    symbol = get_text_filter(_("symbol"), placeholder=_("symbol"))
    code = get_text_filter(_("code"), placeholder=_("code"))
    fraction_name = get_text_filter(
        _("fraction name"),
        placeholder=_("fraction name"),
    )
    is_primary = filters.ChoiceFilter(
        choices=models.Currency.IsPrimaryChoices.choices,
        label=_("is primary"),
    )

    class Meta:
        model = models.Currency
        fields = (
            "name",
            "symbol",
            "code",
            "fraction_name",
            "decimal_places_from",
            "decimal_places_to",
            "is_primary",
            "description",
        )


class APICurrencyFilter(BaseCurrencyFilter):
    pass


class CurrencyFilter(BaseCurrencyFilter):
    pass
