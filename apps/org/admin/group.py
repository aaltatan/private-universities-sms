from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import job_types


@admin.register(models.Group)
class GroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = job_types.SEARCH_FIELDS
    list_per_page = 20
