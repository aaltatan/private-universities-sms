import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseTaxBracketsFilter(BaseNameDescriptionFilter):
    tax = filters.ModelChoiceFilter(
        field_name="tax__name",
        queryset=models.Tax.objects.filter(fixed=False),
        label=_("tax"),
    )
    amount_from_from, amount_from_to = get_number_from_to_filters("amount_from")
    amount_to_from, amount_to_to = get_number_from_to_filters("amount_to")
    rate_from, rate_to = get_number_from_to_filters("rate")
    notes = get_text_filter(label=_("notes").title())

    class Meta:
        model = models.TaxBracket
        fields = (
            "tax",
            "amount_from_from",
            "amount_from_to",
            "amount_to_from",
            "amount_to_to",
            "rate_from",
            "rate_to",
            "notes",
        )


class APITaxBracketsFilter(FilterComboboxMixin, BaseTaxBracketsFilter):
    pass


class TaxBracketFilter(FilterComboboxMixin, BaseTaxBracketsFilter):
    pass
