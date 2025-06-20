from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class CityResource(BaseResource):
    governorate = fields.Field(
        attribute="governorate__name",
        column_name=_("governorate").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )

    def dehydrate_kind(self, obj: models.City):
        return self._dehydrate_choices(obj, "kind")

    class Meta:
        model = models.City
        fields = (
            "serial",
            "name",
            "kind",
            "employees_count",
            "governorate",
            "description",
            "slug",
        )
