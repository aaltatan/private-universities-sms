from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class CostCenterResource(BaseResource):
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    class Meta:
        model = models.CostCenter
        fields = (
            "serial",
            "name",
            "accounting_id",
            "employees_count",
            "description",
            "slug",
        )
