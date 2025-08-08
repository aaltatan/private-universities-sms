from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.core.utils import badge_component
from apps.core.choices import RoundMethodChoices

from .. import models  # , resources
from ..constants import compensations as constants


@admin.register(models.Compensation)
class CompensationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "tax",
        "kind",
        "formatted_calculation_method",
        "value",
        "formatted_round_method",
        "rounded_to",
        "is_active",
    )
    fields = (
        ("name", "shortname", "kind"),
        "calculation_method",
        ("value", "min_value", "max_value"),
        ("min_total", "restrict_to_min_total_value"),
        "min_total_formula",
        ("max_total", "restrict_to_max_total_value"),
        "max_total_formula",
        "formula",
        ("round_method", "rounded_to"),
        ("tax", "tax_classification"),
        ("affected_by_working_days", "is_active"),
        "accounting_id",
        "description",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20

    # resource_classes = (resources.TaxResource,)
    @admin.display(description="Calculation method")
    def formatted_calculation_method(self, obj: models.Compensation) -> str:
        colors = {
            obj.CalculationChoices.BY_INPUT: "blue",
            obj.CalculationChoices.FIXED: "green",
            obj.CalculationChoices.FORMULA: "orangered",
        }
        return badge_component(
            background_color=colors[obj.calculation_method],
            text=obj.get_calculation_method_display(),
            title=obj.formula,
        )

    @admin.display(description="round method")
    def formatted_round_method(self, obj: models.Compensation) -> str:
        colors = {
            RoundMethodChoices.CEIL: "green",
            RoundMethodChoices.FLOOR: "red",
            RoundMethodChoices.ROUND: "blue",
        }
        return badge_component(
            background_color=colors[obj.round_method],
            text=obj.get_round_method_display(),
            title=obj.rounded_to,
        )
