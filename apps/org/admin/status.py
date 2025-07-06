from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import statuses as constants


@admin.register(models.Status)
class StatusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        ("name", "is_payable", "is_separated"),
        "description",
    )
    list_display = ("id", "name", "is_payable", "is_separated", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.StatusResource,)
