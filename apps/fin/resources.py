from django.utils.translation import gettext as _
from import_export import fields, resources, widgets

from apps.core.resources import BaseResource, DehydrateBooleanMixin, SerialResourceMixin

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


class ExchangeRateResource(
    DehydrateBooleanMixin,
    SerialResourceMixin,
    resources.ModelResource,
):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    currency = fields.Field(
        attribute="currency__name",
        column_name=_("currency").title(),
    )
    code = fields.Field(
        attribute="currency__code",
        column_name=_("code").title(),
    )
    created_at = fields.Field(
        attribute="created_at",
        column_name=_("created at").title(),
        widget=widgets.DateTimeWidget(coerce_to_string=False),
    )
    updated_at = fields.Field(
        attribute="updated_at",
        column_name=_("updated at").title(),
        widget=widgets.DateTimeWidget(coerce_to_string=False),
    )
    date = fields.Field(
        attribute="date",
        column_name=_("date").title(),
        widget=widgets.DateWidget(coerce_to_string=False),
    )
    rate = fields.Field(
        attribute="rate",
        column_name=_("rate").title(),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )
    is_primary = fields.Field(
        attribute="currency__is_primary",
        column_name=_("is primary").title(),
    )
    slug = fields.Field(
        attribute="slug",
        column_name=_("slug").title(),
    )

    def dehydrate_is_primary(self, obj: models.ExchangeRate) -> bool:
        return self._dehydrate_boolean(obj.currency.is_primary)

    class Meta:
        model = models.ExchangeRate
        fields = (
            "serial",
            "currency",
            "code",
            "created_at",
            "updated_at",
            "date",
            "rate",
            "is_primary",
            "notes",
            "slug",
        )
