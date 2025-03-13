from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import cities as constants


@admin.register(models.City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "kind",
        "governorate__name",
        "ordering",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    list_filter = ("governorate__name",)
    autocomplete_fields = ("governorate",)
    actions = ("reset_ordering",)

    @admin.action(description="Reset ordering for selected Cities")
    def reset_ordering(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(ordering=0)
