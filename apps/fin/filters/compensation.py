import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_number_from_to_filters,
)

from .. import models


class BaseCompensationFilter(BaseQSearchFilter, BaseNameDescriptionFilter):
    calculation_method = filters.ChoiceFilter(
        field_name="calculation_method",
        label=_("calculation method"),
        choices=models.Compensation.CalculationUserChoices,
    )
    affected_by_working_days = filters.ChoiceFilter(
        field_name="affected_by_working_days",
        label=_("affected by working days"),
        choices=models.Compensation.AffectedByWorkingDaysChoices,
    )
    is_active = filters.ChoiceFilter(
        field_name="is_active",
        label=_("is active"),
        choices=models.Compensation.AffectedByWorkingDaysChoices,
    )
    value_from, value_to = get_number_from_to_filters("value")
    min_value_from, min_value_to = get_number_from_to_filters("min_value")
    max_value_from, max_value_to = get_number_from_to_filters("max_value")

    class Meta:
        model = models.Compensation
        fields = (
            "name",
            "shortname",
            "calculation_method",
            "value_from",
            "value_to",
            "min_value_from",
            "min_value_to",
            "max_value_from",
            "max_value_to",
            "tax",
            "tax_classification",
            "round_method",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
        )


class APICompensationsFilter(BaseCompensationFilter):
    pass


class CompensationFilter(BaseCompensationFilter):
    pass
