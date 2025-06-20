from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class GroupResource(BaseResource):
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    def dehydrate_kind(self, obj: models.Group):
        return self._dehydrate_choices(obj, "kind")

    class Meta:
        model = models.Group
        fields = (
            "serial",
            "name",
            "kind",
            "employees_count",
            "description",
            "slug",
        )
