from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import currencies as constants


@admin.register(models.Currency)
class CurrencyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "symbol",
        "code",
        "is_primary",
        "fraction_name",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    readonly_fields = ("is_primary",)
    resource_classes = (resources.CurrencyResource,)

    def has_delete_permission(self, request, obj: models.Currency | None = None):
        if obj and obj.is_primary:
            return False
        return super().has_delete_permission(request, obj)
