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
    address = fields.Field(
        attribute="address",
        column_name=_("address").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
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
            "address",
            "employees_count",
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
    schools_count = fields.Field(
        attribute="schools_count",
        column_name=_("schools count").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
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


class SpecializationResource(BaseResource):
    is_specialist = fields.Field(
        attribute="is_specialist",
        column_name=_("specialist?").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
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
