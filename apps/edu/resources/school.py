from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class SchoolResource(BaseResource):
    kind = fields.Field(
        attribute="kind__name",
        column_name=_("kind"),
    )
    nationality = fields.Field(
        attribute="nationality__name",
        column_name=_("nationality"),
    )
    website = fields.Field(
        attribute="website",
        column_name=_("website"),
    )
    phone = fields.Field(
        attribute="phone",
        column_name=_("phone"),
    )
    email = fields.Field(
        attribute="email",
        column_name=_("email"),
    )
    address = fields.Field(
        attribute="address",
        column_name=_("address"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
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
