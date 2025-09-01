from django.utils.translation import gettext_lazy as _
from import_export import fields, resources, widgets

from apps.core.resources import SerialResourceMixin

from .. import models


class TaxBracketResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    tax = fields.Field(
        attribute="tax__name",
        column_name=_("tax"),
    )
    amount_from = fields.Field(
        attribute="amount_from",
        column_name=_("amount from"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    amount_to = fields.Field(
        attribute="amount_to",
        column_name=_("amount to"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    rate = fields.Field(
        attribute="rate",
        column_name=_("rate"),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes"),
    )

    class Meta:
        model = models.TaxBracket
        fields = (
            "serial",
            "tax",
            "amount_from",
            "amount_to",
            "rate",
            "notes",
            "slug",
        )
