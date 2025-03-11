from django.contrib import admin
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
        "description",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("governorate",)
