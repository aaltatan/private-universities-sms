from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import currencies as constants


@admin.register(models.ExchangeRate)
class ExchangeRateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "currency__name",
        "created_at",
        "date",
        "rate",
        "slug",
    )
    list_display_links = ("id", "currency__name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.ExchangeRateResource,)

    def has_change_permission(
        self,
        request,
        obj: models.ExchangeRate | None = None,
    ):
        if obj and obj.currency.is_primary:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(
        self,
        request,
        obj: models.ExchangeRate | None = None,
    ):
        if obj and obj.currency.is_primary:
            return False
        return super().has_delete_permission(request, obj)
