from django.utils.translation import gettext as _

from import_export import resources, fields

from . import models


class BaseResource(resources.ModelResource):
    name = fields.Field(
        attribute="name",
        column_name=_("name").title(),
    )
    description = fields.Field(
        attribute="description",
        column_name=_("description").title(),
    )
    slug = fields.Field(
        attribute="slug",
        column_name=_("slug").title(),
    )


class GovernorateResource(BaseResource):
    class Meta:
        model = models.Governorate


class CityResource(BaseResource):
    governorate = fields.Field(
        attribute="governorate__name",
        column_name=_("governorate").title(),
    )

    class Meta:
        model = models.City
        fields = ("id", "name", "governorate", "description", "slug")
