from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseTaxBracketFilter(BaseNameDescriptionFilter):
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


class APITaxBracketFilter(FilterComboboxMixin, BaseTaxBracketFilter):
    tax = get_combobox_choices_filter(
        queryset=models.Tax.objects.filter(
            calculation_method=models.Tax.CalculationMethodChoices.BRACKETS
        ),
        field_name="name",
        label=_("tax"),
    )


class TaxBracketFilter(FilterComboboxMixin, BaseTaxBracketFilter):
    tax = get_combobox_choices_filter(
        queryset=models.Tax.objects.filter(
            calculation_method=models.Tax.CalculationMethodChoices.BRACKETS
        ),
        field_name="name",
        label=_("tax"),
        api_filter=True,
    )
