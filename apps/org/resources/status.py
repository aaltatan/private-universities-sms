from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class StatusResource(BaseResource):
    is_payable = fields.Field(
        attribute="is_payable",
        column_name=_("is payable"),
    )
    is_separated = fields.Field(
        attribute="is_separated",
        column_name=_("is separated"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
    )

    def dehydrate_is_payable(self, obj: models.Status):
        return self._dehydrate_boolean(obj.is_payable)

    class Meta:
        model = models.Status
        fields = (
            "serial",
            "name",
            "is_payable",
            "is_separated",
            "employees_count",
            "description",
            "slug",
        )
