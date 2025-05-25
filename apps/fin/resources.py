from django.utils.translation import gettext as _
from import_export import fields, resources, widgets

from apps.core.resources import BaseResource, SerialResourceMixin

from . import models


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


class YearResource(BaseResource):
    class Meta:
        model = models.Year
        fields = ("serial", "name", "description", "slug")


class TaxResource(BaseResource):
    def dehydrate_is_closed(self, obj: models.Tax):
        return self._dehydrate_boolean(obj.fixed)

    class Meta:
        model = models.Tax
        fields = (
            "serial",
            "name",
            "fixed",
            "rate",
            "rounded_to",
            "round_method",
            "description",
            "slug",
        )


class TaxBracketResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    tax = fields.Field(
        attribute="tax__name",
        column_name=_("tax").title(),
    )
    amount_from = fields.Field(
        attribute="amount_from",
        column_name=_("amount from").title(),
    )
    amount_to = fields.Field(
        attribute="amount_to",
        column_name=_("amount to").title(),
    )
    rate = fields.Field(
        attribute="rate",
        column_name=_("rate").title(),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )

    class Meta:
        model = models.TaxBracket
        fields = (
            "serial",
            "tax",
            "amount_from",
            "amount_to",
            "rate",
            "notes",
            "slug",
        )
