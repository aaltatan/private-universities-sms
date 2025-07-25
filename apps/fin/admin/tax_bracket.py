from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import tax_brackets as constants


@admin.register(models.TaxBracket)
class TaxBracketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        "tax",
        ("amount_from", "amount_to", "rate"),
        "notes",
    )
    list_display = ("id", "tax__name", "amount_from", "amount_to", "rate", "slug")
    list_display_links = ("id", "tax__name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.TaxBracketResource,)
    autocomplete_fields = ("tax",)
