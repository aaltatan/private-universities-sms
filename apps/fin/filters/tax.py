import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_number_from_to_filters,
)

from .. import models


class BaseTaxesFilter(BaseNameDescriptionFilter):
    fixed = filters.ChoiceFilter(
        label=_("fixed").title(),
        choices=models.Tax.FixedChoices,
    )
    rate_from, rate_to = get_number_from_to_filters("rate")

    class Meta:
        model = models.Tax
        fields = (
            "name",
            "fixed",
            "rate_from",
            "rate_to",
            "description",
        )


class APITaxesFilter(FilterComboboxMixin, BaseTaxesFilter):
    pass


class TaxFilter(FilterComboboxMixin, BaseTaxesFilter):
    pass
