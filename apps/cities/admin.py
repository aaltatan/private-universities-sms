from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models, constants


@admin.register(models.City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "governorate__name", "slug")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("governorate",)
