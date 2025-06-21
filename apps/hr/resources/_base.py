from django.utils.translation import gettext as _
from import_export import fields, resources

from apps.core.resources import SerialResourceMixin


class BaseInfoResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    employee_name = fields.Field(
        attribute="employee__fullname",
        column_name=_("employee name").title(),
    )
    employee_national_id = fields.Field(
        attribute="employee__national_id",
        column_name=_("employee national id").title(),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )
