from django.utils.translation import gettext as _
from import_export import fields, widgets

from apps.core.resources import BaseResource

from .. import models


class CompensationResource(BaseResource):
    shortname = fields.Field(
        attribute="shortname",
        column_name=_("short name").title(),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )
    calculation_method = fields.Field(
        attribute="calculation_method",
        column_name=_("calculation method").title(),
    )
    tax = fields.Field(
        attribute="tax__name",
        column_name=_("tax").title(),
    )
    tax_classification = fields.Field(
        attribute="tax_classification",
        column_name=_("tax classification").title(),
    )
    round_method = fields.Field(
        attribute="round_method",
        column_name=_("round method").title(),
    )
    rounded_to = fields.Field(
        attribute="rounded_to",
        column_name=_("rounded to").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    value = fields.Field(
        attribute="value",
        column_name=_("value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    min_value = fields.Field(
        attribute="min_value",
        column_name=_("min value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    max_value = fields.Field(
        attribute="max_value",
        column_name=_("max value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    min_total = fields.Field(
        attribute="min_total",
        column_name=_("min total value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    max_total = fields.Field(
        attribute="max_total",
        column_name=_("max total value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    restricted_min_total_value = fields.Field(
        attribute="restrict_to_min_total_value",
        column_name=_("restrict to min total value").title(),
    )
    restricted_max_total_value = fields.Field(
        attribute="restrict_to_max_total_value",
        column_name=_("restrict to max total value").title(),
    )
    affected_by_working_days = fields.Field(
        attribute="affected_by_working_days",
        column_name=_("affected by working days").title(),
    )
    is_active = fields.Field(
        attribute="is_active",
        column_name=_("is active").title(),
    )
    formula = fields.Field(
        attribute="formula",
        column_name=_("formula").title(),
    )
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id").title(),
    )

    def dehydrate_calculation_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "calculation_method")

    def dehydrate_kind(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "kind")

    def dehydrate_tax_classification(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "tax_classification")

    def dehydrate_round_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "round_method")

    def dehydrate_affected_by_working_days(self, obj: models.Compensation):
        return self._dehydrate_boolean(obj.affected_by_working_days)

    def dehydrate_is_active(self, obj: models.Compensation):
        return self._dehydrate_boolean(obj.is_active)

    class Meta:
        model = models.Compensation
        fields = (
            "serial",
            "name",
            "shortname",
            "kind",
            "calculation_method",
            "tax",
            "tax_classification",
            "round_method",
            "rounded_to",
            "value",
            "min_value",
            "max_value",
            "min_total",
            "restrict_to_min_total_value",
            "max_total",
            "restrict_to_max_total_value",
            "formula",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
            "slug",
        )
