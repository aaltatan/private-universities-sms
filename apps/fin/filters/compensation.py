import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_number_from_to_filters,
)

from .. import models


class BaseCompensationFilter(BaseQSearchFilter, BaseNameDescriptionFilter):
    kind = filters.ChoiceFilter(
        field_name="kind",
        label=_("kind"),
        choices=models.Compensation.CompensationKindChoices,
    )
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
    min_total_from, min_total_to = get_number_from_to_filters("min_total")
    max_total_from, max_total_to = get_number_from_to_filters("max_total")
    restrict_to_min_total_value = filters.ChoiceFilter(
        field_name="restrict_to_min_total_value",
        label=_("restrict to min total value"),
        choices=models.Compensation.RestrictionChoices,
    )
    restrict_to_max_total_value = filters.ChoiceFilter(
        field_name="restrict_to_max_total_value",
        label=_("restrict to max total value"),
        choices=models.Compensation.RestrictionChoices,
    )

    class Meta:
        model = models.Compensation
        fields = (
            "name",
            "shortname",
            "kind",
            "calculation_method",
            "value_from",
            "value_to",
            "min_value_from",
            "min_value_to",
            "max_value_from",
            "max_value_to",
            "min_total_from",
            "min_total_to",
            "restrict_to_min_total_value",
            "max_total_from",
            "max_total_to",
            "restrict_to_max_total_value",
            "tax",
            "tax_classification",
            "round_method",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
        )


class APICompensationFilter(BaseCompensationFilter):
    pass


class CompensationFilter(BaseCompensationFilter):
    pass
