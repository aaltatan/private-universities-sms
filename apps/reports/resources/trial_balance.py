from django.utils.translation import gettext as _
from import_export import fields, resources

from apps.core.resources import SerialResourceMixin
from apps.hr.models import Employee


class TrialBalanceResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    fullname = fields.Field(
        attribute="fullname",
        column_name=_("fullname").title(),
    )

    class Meta:
        model = Employee
        fields = (
            "serial",
            "fullname",
        )
