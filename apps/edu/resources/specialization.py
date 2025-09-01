from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class SpecializationResource(BaseResource):
    is_specialist = fields.Field(
        attribute="is_specialist",
        column_name=_("specialist?"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
    )

    def dehydrate_is_specialist(self, obj: models.Specialization) -> str:
        return self._dehydrate_boolean(obj.is_specialist)

    class Meta:
        model = models.Specialization
        fields = (
            "serial",
            "name",
            "is_specialist",
            "description",
            "employees_count",
            "slug",
        )
