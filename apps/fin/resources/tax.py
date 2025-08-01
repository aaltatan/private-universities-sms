from django.utils.translation import gettext as _
from import_export import fields, widgets

from apps.core.resources import BaseResource

from .. import models


class TaxResource(BaseResource):
    shortname = fields.Field(
        attribute="shortname",
        column_name=_("short name").title(),
    )
    calculation_method = fields.Field(
        attribute="calculation_method",
        column_name=_("calculation method").title(),
        dehydrate_method="dehydrate_calculation_method",
    )
    amount = fields.Field(
        attribute="amount",
        column_name=_("amount").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    percentage = fields.Field(
        attribute="percentage",
        column_name=_("percentage").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    formula = fields.Field(
        attribute="formula",
        column_name=_("formula").title(),
    )
    rounded_to = fields.Field(
        attribute="rounded_to",
        column_name=_("rounded to").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    round_method = fields.Field(
        attribute="round_method",
        column_name=_("round method").title(),
    )
    affected_by_working_days = fields.Field(
        attribute="affected_by_working_days",
        column_name=_("affected by working days").title(),
    )
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id").title(),
    )
    description = fields.Field(
        attribute="description",
        column_name=_("description").title(),
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
