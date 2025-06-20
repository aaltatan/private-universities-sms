from django.utils.translation import gettext as _
from import_export import fields, widgets

from apps.core.resources import BaseResource

from .. import models


class PeriodResource(BaseResource):
    year = fields.Field(
        attribute="year__name",
        column_name=_("year").title(),
    )
    start_date = fields.Field(
        attribute="start_date",
        column_name=_("birth date").title(),
        widget=widgets.DateWidget(coerce_to_string=False),
    )
    is_closed = fields.Field(
        attribute="is_closed",
        column_name=_("is closed").title(),
    )

    def dehydrate_is_closed(self, obj: models.Period):
        return self._dehydrate_boolean(obj.is_closed)

    class Meta:
        model = models.Period
        fields = (
            "serial",
            "name",
            "year",
            "start_date",
            "is_closed",
            "description",
            "slug",
        )
