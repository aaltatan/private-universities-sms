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
