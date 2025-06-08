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
    fixed = fields.Field(
        attribute="fixed",
        column_name=_("fixed").title(),
    )
    rate = fields.Field(
        attribute="rate",
        column_name=_("rate").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    rounded_to = fields.Field(
        attribute="rounded_to",
        column_name=_("rounded to").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    round_method = fields.Field(
        attribute="round_method",
        column_name=_("round method").title(),
    )

    def dehydrate_round_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "round_method")

    def dehydrate_fixed(self, obj: models.Tax):
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
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    amount_to = fields.Field(
        attribute="amount_to",
        column_name=_("amount to").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    rate = fields.Field(
        attribute="rate",
        column_name=_("rate").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
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


class CompensationResource(BaseResource):
    shortname = fields.Field(
        attribute="shortname",
        column_name=_("short name").title(),
    )
    calculation_method = fields.Field(
        attribute="calculation_method",
        column_name=_("calculation method").title(),
    )
    tax = fields.Field(
        attribute="tax__name",
        column_name=_("tax").title(),
    )
    tax_classification = fields.Field(
        attribute="tax_classification",
        column_name=_("tax classification").title(),
    )
    round_method = fields.Field(
        attribute="round_method",
        column_name=_("round method").title(),
    )
    rounded_to = fields.Field(
        attribute="rounded_to",
        column_name=_("rounded to").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    value = fields.Field(
        attribute="value",
        column_name=_("value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    min_value = fields.Field(
        attribute="min_value",
        column_name=_("min value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    max_value = fields.Field(
        attribute="max_value",
        column_name=_("max value").title(),
        widget=widgets.DecimalWidget(coerce_to_string=False),
    )
    affected_by_working_days = fields.Field(
        attribute="affected_by_working_days",
        column_name=_("affected by working days").title(),
    )
    is_active = fields.Field(
        attribute="is_active",
        column_name=_("is active").title(),
    )
    formula = fields.Field(
        attribute="formula",
        column_name=_("formula").title(),
    )
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id").title(),
    )

    def dehydrate_calculation_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "calculation_method")

    def dehydrate_tax_classification(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "tax_classification")

    def dehydrate_round_method(self, obj: models.Compensation):
        return self._dehydrate_choices(obj, "round_method")

    def dehydrate_affected_by_working_days(self, obj: models.Compensation):
        return self._dehydrate_boolean(obj.affected_by_working_days)

    def dehydrate_is_active(self, obj: models.Compensation):
        return self._dehydrate_boolean(obj.is_active)

    class Meta:
        model = models.Compensation
        fields = (
            "serial",
            "name",
            "shortname",
            "calculation_method",
            "tax",
            "tax_classification",
            "round_method",
            "rounded_to",
            "value",
            "min_value",
            "max_value",
            "formula",
            "affected_by_working_days",
            "is_active",
            "accounting_id",
            "description",
            "slug",
        )


class VoucherKindResource(BaseResource):
    class Meta:
        model = models.VoucherKind
        fields = ("serial", "name", "description", "slug")
