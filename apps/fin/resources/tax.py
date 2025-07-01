from django.utils.translation import gettext as _
from import_export import fields, widgets

from apps.core.resources import BaseResource

from .. import models


class TaxResource(BaseResource):
    fixed = fields.Field(
        attribute="fixed",
        column_name=_("fixed").title(),
    )
    rate = fields.Field(
        attribute="rate",
        column_name=_("rate").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
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
    description = fields.Field(
        attribute="description",
        column_name=_("description").title(),
    )

    def dehydrate_affected_by_working_days(self, obj: models.Compensation):
        return self._dehydrate_boolean(obj.affected_by_working_days)

    def dehydrate_round_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "round_method")

    def dehydrate_fixed(self, obj: models.Tax):
        return self._dehydrate_boolean(obj.fixed)

    class Meta:
        model = models.Tax
        fields = (
            "serial",
            "name",
            "fixed",
            "rate",
            "rounded_to",
            "round_method",
            "affected_by_working_days",
            "description",
            "slug",
        )
