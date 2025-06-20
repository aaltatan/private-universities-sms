from django.utils.translation import gettext as _
from import_export import fields, resources

from .. import models
from ._base import BaseInfoResource


class PhoneResource(BaseInfoResource, resources.ModelResource):
    number = fields.Field(
        attribute="number",
        column_name=_("number").title(),
    )

    class Meta:
        model = models.Phone
        fields = (
            "serial",
            "employee_name",
            "employee_national_id",
            "number",
            "kind",
            "notes",
        )
