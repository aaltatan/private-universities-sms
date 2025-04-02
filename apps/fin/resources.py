from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class CurrencyResource(BaseResource):
    symbol = fields.Field(
        attribute="symbol",
        column_name=_("symbol").title(),
    )
    code = fields.Field(
        attribute="code",
        column_name=_("code").title(),
    )
    fraction_name = fields.Field(
        attribute="fraction_name",
        column_name=_("fraction name").title(),
    )
    decimal_places = fields.Field(
        attribute="decimal_places",
        column_name=_("decimal places").title(),
    )
    is_primary = fields.Field(
        attribute="is_primary",
        column_name=_("is primary").title(),
    )

    def dehydrate_is_primary(self, obj: models.Currency) -> bool:
        return self._dehydrate_boolean(obj.is_primary)

    class Meta:
        model = models.Currency
        fields = (
            "serial",
            "name",
            "symbol",
            "code",
            "fraction_name",
            "decimal_places",
            "is_primary",
            "description",
            "slug",
        )
