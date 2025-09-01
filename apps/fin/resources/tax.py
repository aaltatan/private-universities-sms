from django.utils.translation import gettext_lazy as _
from import_export import fields, widgets

from apps.core.resources import BaseResource

from .. import models


class TaxResource(BaseResource):
    shortname = fields.Field(
        attribute="shortname",
        column_name=_("short name"),
    )
    calculation_method = fields.Field(
        attribute="calculation_method",
        column_name=_("calculation method"),
        dehydrate_method="dehydrate_calculation_method",
    )
    amount = fields.Field(
        attribute="amount",
        column_name=_("amount"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    percentage = fields.Field(
        attribute="percentage",
        column_name=_("percentage"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    formula = fields.Field(
        attribute="formula",
        column_name=_("formula"),
    )
    rounded_to = fields.Field(
        attribute="rounded_to",
        column_name=_("rounded to"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    round_method = fields.Field(
        attribute="round_method",
        column_name=_("round method"),
    )
    affected_by_working_days = fields.Field(
        attribute="affected_by_working_days",
        column_name=_("affected by working days"),
    )
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id"),
    )
    description = fields.Field(
        attribute="description",
        column_name=_("description"),
    )

    def dehydrate_affected_by_working_days(self, obj: models.Compensation):
        return self._dehydrate_boolean(obj.affected_by_working_days)

    def dehydrate_round_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "round_method")

    def dehydrate_calculation_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "calculation_method")

    class Meta:
        model = models.Tax
        fields = (
            "serial",
            "name",
            "shortname",
            "calculation_method",
            "amount",
            "percentage",
            "formula",
            "rounded_to",
            "round_method",
            "accounting_id",
            "affected_by_working_days",
            "description",
            "slug",
        )
