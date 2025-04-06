from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import currencies as constants


class ExchangeRateInline(admin.TabularInline):
    model = models.ExchangeRate
    fields = ("date", "rate")

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.is_primary:
            return 0
        return 1

    def get_max_num(self, request, obj=None, **kwargs):
        if obj and obj.is_primary:
            return 1
        return super().get_max_num(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_primary:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_primary:
            return False
        return super().has_delete_permission(request, obj)


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
    inlines = (ExchangeRateInline,)

    def has_delete_permission(self, request, obj: models.Currency | None = None):
        if obj and obj.is_primary:
            return False
        return super().has_delete_permission(request, obj)
