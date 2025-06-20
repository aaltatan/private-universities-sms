from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class DegreeResource(BaseResource):
    is_academic = fields.Field(
        attribute="is_academic",
        column_name=_("academic?").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    def dehydrate_is_academic(self, obj: models.Degree) -> str:
        return self._dehydrate_boolean(obj.is_academic)

    class Meta:
        model = models.Degree
        fields = (
            "serial",
            "name",
            "is_academic",
            "employees_count",
            "description",
            "slug",
        )
