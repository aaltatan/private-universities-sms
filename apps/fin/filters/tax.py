import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_number_from_to_filters,
)

from .. import models


class BaseTaxFilter(BaseNameDescriptionFilter):
    fixed = filters.ChoiceFilter(
        label=_("fixed").title(),
        choices=models.Tax.FixedChoices,
    )
    affected_by_working_days = filters.ChoiceFilter(
        label=_("affected by working days").title(),
        choices=models.Tax.AffectedByWorkingDaysChoices,
    )
    rate_from, rate_to = get_number_from_to_filters("rate")

    class Meta:
        model = models.Tax
        fields = (
            "name",
            "fixed",
            "rate_from",
            "rate_to",
            "affected_by_working_days",
            "description",
        )


class APITaxFilter(FilterComboboxMixin, BaseTaxFilter):
    pass


class TaxFilter(FilterComboboxMixin, BaseTaxFilter):
    pass
