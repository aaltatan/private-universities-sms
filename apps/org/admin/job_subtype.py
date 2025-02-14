from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import job_subtypes


@admin.register(models.JobSubtype)
class JobSubtypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "job_type__name", "slug")
    list_display_links = ("id", "name")
    search_fields = job_subtypes.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("job_type",)
