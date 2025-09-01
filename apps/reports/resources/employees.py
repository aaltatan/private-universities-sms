from django.utils.translation import gettext_lazy as _
from import_export import fields, resources, widgets

from apps.core.resources import SerialResourceMixin
from apps.hr.models import Employee


class EmployeeResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    uuid = fields.Field(
        attribute="uuid",
        column_name=_("uuid"),
    )
    fullname = fields.Field(
        attribute="fullname",
        column_name=_("fullname"),
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
        model = Employee
        fields = (
            "serial",
            "uuid",
            "fullname",
            "total_debit",
            "total_credit",
            "total_amount",
        )
