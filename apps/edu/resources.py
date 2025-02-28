from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class SchoolResource(BaseResource):
    kind = fields.Field(
        attribute="kind__name",
        column_name=_("kind").title(),
    )
    nationality = fields.Field(
        attribute="nationality__name",
        column_name=_("nationality").title(),
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

    class Meta:
        model = models.School
        fields = (
            "serial",
            "name",
            "kind",
            "nationality",
            "website",
            "email",
            "phone",
            "description",
            "slug",
        )


class SchoolKindResource(BaseResource):
    is_governmental = fields.Field(
        attribute="is_governmental",
        column_name=_("governmental?").title(),
    )
    is_virtual = fields.Field(
        attribute="is_virtual",
        column_name=_("virtual?").title(),
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
            "description",
            "slug",
        )


class SpecializationResource(BaseResource):
    is_specialist = fields.Field(
        attribute="is_specialist",
        column_name=_("specialist?").title(),
    )

    def dehydrate_is_specialist(self, obj: models.Specialization) -> str:
        return self._dehydrate_boolean(obj.is_specialist)

    class Meta:
        model = models.Specialization
        fields = ("serial", "name", "is_specialist", "description", "slug")


class DegreeResource(BaseResource):
    is_academic = fields.Field(
        attribute="is_academic",
        column_name=_("academic?").title(),
    )

    def dehydrate_is_academic(self, obj: models.Degree) -> str:
        return self._dehydrate_boolean(obj.is_academic)

    class Meta:
        model = models.Degree
        fields = ("serial", "name", "is_academic", "description", "slug")
