from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class GovernorateResource(BaseResource):
    class Meta:
        model = models.Governorate
        fields = ("serial", "name", "description", "slug")


class CityResource(BaseResource):
    governorate = fields.Field(
        attribute="governorate__name",
        column_name=_("governorate").title(),
    )

    class Meta:
        model = models.City
        fields = ("serial", "name", "governorate", "description", "slug")


class NationalityResource(BaseResource):
    is_local = fields.Field(
        attribute="is_local",
        column_name=_("is local").title(),
    )

    def dehydrate_is_local(self, value: bool):
        return _("yes").title() if value else _("no").title()

    class Meta:
        model = models.Nationality
        fields = ("serial", "name", "is_local", "description", "slug")
