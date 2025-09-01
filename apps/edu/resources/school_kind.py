from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class SchoolKindResource(BaseResource):
    is_governmental = fields.Field(
        attribute="is_governmental",
        column_name=_("governmental?"),
    )
    is_virtual = fields.Field(
        attribute="is_virtual",
        column_name=_("virtual?"),
    )
    schools_count = fields.Field(
        attribute="schools_count",
        column_name=_("schools count"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
    )

    def dehydrate_is_governmental(self, obj: models.SchoolKind) -> str:
        return self._dehydrate_boolean(obj.is_governmental)

    def dehydrate_is_virtual(self, obj: models.SchoolKind) -> str:
        return self._dehydrate_boolean(obj.is_virtual)

    class Meta:
        model = models.SchoolKind
        fields = (
            "serial",
            "name",
            "is_governmental",
            "is_virtual",
            "schools_count",
            "employees_count",
            "description",
            "slug",
        )
