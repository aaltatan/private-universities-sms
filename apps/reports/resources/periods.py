from django.utils.translation import gettext_lazy as _
from import_export import fields, resources, widgets

from apps.core.resources import SerialResourceMixin
from apps.fin.models import Period


class PeriodResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    period = fields.Field(
        attribute="name",
        column_name=_("period"),
    )
    total_debit = fields.Field(
        attribute="total_debit",
        column_name=_("total debit"),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    total_credit = fields.Field(
        attribute="total_credit",
        column_name=_("total credit"),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    total_amount = fields.Field(
        attribute="total_amount",
        column_name=_("net"),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )

    class Meta:
        model = Period
        fields = (
            "serial",
            "period",
            "total_debit",
            "total_credit",
            "total_amount",
        )
