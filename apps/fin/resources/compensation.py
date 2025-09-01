from django.utils.translation import gettext_lazy as _
from import_export import fields, widgets

from apps.core.resources import BaseResource

from .. import models


class CompensationResource(BaseResource):
    shortname = fields.Field(
        attribute="shortname",
        column_name=_("short name"),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind"),
    )
    calculation_method = fields.Field(
        attribute="calculation_method",
        column_name=_("calculation method"),
    )
    tax = fields.Field(
        attribute="tax__name",
        column_name=_("tax"),
    )
    tax_classification = fields.Field(
        attribute="tax_classification",
        column_name=_("tax classification"),
    )
    round_method = fields.Field(
        attribute="round_method",
        column_name=_("round method"),
    )
    rounded_to = fields.Field(
        attribute="rounded_to",
        column_name=_("rounded to"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    value = fields.Field(
        attribute="value",
        column_name=_("value"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    min_value = fields.Field(
        attribute="min_value",
        column_name=_("min value"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    max_value = fields.Field(
        attribute="max_value",
        column_name=_("max value"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    min_total = fields.Field(
        attribute="min_total",
        column_name=_("min total value"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    max_total = fields.Field(
        attribute="max_total",
        column_name=_("max total value"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    restrict_to_min_total_value = fields.Field(
        attribute="restrict_to_min_total_value",
        column_name=_("restrict to min total value"),
    )
    restrict_to_max_total_value = fields.Field(
        attribute="restrict_to_max_total_value",
        column_name=_("restrict to max total value"),
    )
    min_total_formula = fields.Field(
        attribute="min_total_formula",
        column_name=_("min total formula"),
    )
    max_total_formula = fields.Field(
        attribute="max_total_formula",
        column_name=_("max total formula"),
    )
    affected_by_working_days = fields.Field(
        attribute="affected_by_working_days",
        column_name=_("affected by working days"),
    )
    is_active = fields.Field(
        attribute="is_active",
        column_name=_("is active"),
    )
    formula = fields.Field(
        attribute="formula",
        column_name=_("formula"),
    )
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id"),
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
            "min_total_formula",
            "restrict_to_min_total_value",
            "max_total",
            "max_total_formula",
            "restrict_to_max_total_value",
            "formula",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
            "slug",
        )
