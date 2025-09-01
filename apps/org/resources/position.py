from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class PositionResource(BaseResource):
    order = fields.Field(
        attribute="order",
        column_name=_("order"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
    )

    class Meta:
        model = models.Position
        fields = (
            "serial",
            "name",
            "order",
            "employees_count",
            "description",
            "slug",
        )
