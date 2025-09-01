import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseTaxFilter(BaseNameDescriptionFilter):
    shortname = get_text_filter(label=_("short name"))
    calculation_method = filters.ChoiceFilter(
        label=_("calculation method"),
        choices=models.Tax.CalculationMethodChoices,
    )
    affected_by_working_days = filters.ChoiceFilter(
        label=_("affected by working days"),
        choices=models.Tax.AffectedByWorkingDaysChoices,
    )
    amount_from, amount_to = get_number_from_to_filters("amount")
    percentage_from, percentage_to = get_number_from_to_filters("percentage")

    class Meta:
        model = models.Tax
        fields = (
            "name",
            "shortname",
            "calculation_method",
            "amount_from",
            "amount_to",
            "percentage_from",
            "percentage_to",
            "affected_by_working_days",
            "description",
        )


class APITaxFilter(FilterComboboxMixin, BaseTaxFilter):
    pass


class TaxFilter(FilterComboboxMixin, BaseTaxFilter):
    pass
