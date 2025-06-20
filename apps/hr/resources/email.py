from django.utils.translation import gettext as _
from import_export import fields, resources

from .. import models
from ._base import BaseInfoResource


class EmailResource(BaseInfoResource, resources.ModelResource):
    email = fields.Field(
        attribute="email",
        column_name=_("email").title(),
    )

    class Meta:
        model = models.Email
        fields = (
            "serial",
            "employee_name",
            "employee_national_id",
            "email",
            "kind",
            "notes",
        )
