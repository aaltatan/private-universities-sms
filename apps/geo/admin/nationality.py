from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import nationalities


@admin.register(models.Nationality)
class NationalityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "is_local", "slug")
    list_display_links = ("id", "name")
    search_fields = nationalities.SEARCH_FIELDS
    list_per_page = 20
