from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import specialization as constants


@admin.register(models.Specialization)
class SpecializationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_specialist",
        "description",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
