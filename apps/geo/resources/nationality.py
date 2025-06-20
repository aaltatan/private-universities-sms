from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class NationalityResource(BaseResource):
    is_local = fields.Field(
        attribute="is_local",
        column_name=_("is local").title(),
    )

    def dehydrate_is_local(self, obj: models.Nationality):
        return self._dehydrate_boolean(obj.is_local)

    class Meta:
        model = models.Nationality
        fields = ("serial", "name", "is_local", "description", "slug")
