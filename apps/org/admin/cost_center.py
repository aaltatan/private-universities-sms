from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import cost_centers as constants


@admin.register(models.CostCenter)
class CostCenterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        ("name", "accounting_id"),
        "description",
    )
    list_display = ("id", "name", "accounting_id", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.CostCenterResource,)
