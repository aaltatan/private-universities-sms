from django.utils.translation import gettext as _
from import_export import fields, resources, widgets

from apps.core.resources import SerialResourceMixin
from apps.fin.models import Compensation


class CompensationResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    compensation = fields.Field(
        attribute="name",
        column_name=_("compensation").title(),
    )
    total_debit = fields.Field(
        attribute="total_debit",
        column_name=_("total debit").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    total_credit = fields.Field(
        attribute="total_credit",
        column_name=_("total credit").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    total_amount = fields.Field(
        attribute="total_amount",
        column_name=_("net").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )

    class Meta:
        model = Compensation
        fields = (
            "serial",
            "compensation",
            "total_debit",
            "total_credit",
            "total_amount",
        )
