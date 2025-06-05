from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class GovernorateResource(BaseResource):
    cities_count = fields.Field(
        attribute="cities_count",
        column_name=_("cities count").title(),
    )

    class Meta:
        model = models.Governorate
        fields = ("serial", "name", "cities_count", "description", "slug")


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
