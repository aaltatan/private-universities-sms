from django.utils.translation import gettext as _

from import_export import resources, fields

from . import models


class CityResource(resources.ModelResource):
    name = fields.Field(
        attribute='name',
        column_name=_("name").title(),
    )
    governorate = fields.Field(
        attribute='governorate__name',
        column_name=_("governorate").title(),
    )
    description = fields.Field(
        attribute='description',
        column_name=_("description").title(),
    )
    slug = fields.Field(
        attribute='slug',
        column_name=_("slug").title(),
    )

    class Meta:
        model = models.City
        fields = ("id", "name", "governorate", "description", "slug")
