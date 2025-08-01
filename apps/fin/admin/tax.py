from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import taxes as constants


class TaxBracketInline(admin.TabularInline):
    model = models.TaxBracket
    extra = 0
    fields = ("amount_from", "amount_to", "rate")


@admin.register(models.Tax)
class TaxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        ("name", "shortname"),
        "calculation_method",
        ("amount", "percentage"),
        "formula",
        ("rate", "rounded_to", "round_method"),
        ("fixed", "affected_by_working_days"),
        "accounting_id",
        "description",
    )
    list_display = ("id", "name", "calculation_method", "rounded_to", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.TaxResource,)
    inlines = (TaxBracketInline,)
