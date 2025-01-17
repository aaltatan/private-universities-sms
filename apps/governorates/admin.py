from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models, constants


@admin.register(models.Governorate)
class GovernorateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
