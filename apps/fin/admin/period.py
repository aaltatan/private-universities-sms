from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import periods as constants


@admin.register(models.Period)
class PeriodAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "year",
        "start_date",
        "is_closed",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    list_filter = ("is_closed", "year")
    resource_classes = (resources.PeriodResource,)
