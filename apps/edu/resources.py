from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class SchoolResource(BaseResource):
    nationality = fields.Field(
        attribute="nationality__name",
        column_name=_("nationality").title(),
    )
    is_governmental = fields.Field(
        attribute="is_governmental",
        column_name=_("governmental?").title(),
    )
    is_virtual = fields.Field(
        attribute="is_virtual",
        column_name=_("virtual?").title(),
    )
    website = fields.Field(
        attribute="website",
        column_name=_("website").title(),
    )
    phone = fields.Field(
        attribute="phone",
        column_name=_("phone").title(),
    )
    email = fields.Field(
        attribute="email",
        column_name=_("email").title(),
    )

    def dehydrate_is_governmental(self, obj: models.School) -> str:
        return self._dehydrate_boolean(obj.is_governmental)

    def dehydrate_is_virtual(self, obj: models.School) -> str:
        return self._dehydrate_boolean(obj.is_virtual)

    class Meta:
        model = models.School
        fields = (
            "serial",
            "name",
            "nationality",
            "is_governmental",
            "is_virtual",
            "website",
            "email",
            "phone",
            "description",
            "slug",
        )
