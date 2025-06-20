from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


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
