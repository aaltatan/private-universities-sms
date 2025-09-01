from django.utils.translation import gettext_lazy as _
from import_export import fields, resources

from apps.core.resources import DehydrateBooleanMixin

from .. import models
from ._base import BaseInfoResource


class MobileResource(
    BaseInfoResource,
    DehydrateBooleanMixin,
    resources.ModelResource,
):
    number = fields.Field(
        attribute="number",
        column_name=_("number"),
    )
    has_whatsapp = fields.Field(
        attribute="has_whatsapp",
        column_name=_("has whatsapp"),
    )
    whatsapp_url = fields.Field(
        column_name=_("whatsapp url"),
    )

    def dehydrate_has_whatsapp(self, obj: models.Mobile):
        return self._dehydrate_boolean(obj.has_whatsapp)

    def dehydrate_whatsapp_url(self, obj: models.Mobile):
        if obj.has_whatsapp:
            return obj.get_whatsapp_url()
        return ""

    class Meta:
        model = models.Mobile
        fields = (
            "serial",
            "employee_name",
            "employee_national_id",
            "number",
            "kind",
            "has_whatsapp",
            "whatsapp_url",
            "notes",
        )
