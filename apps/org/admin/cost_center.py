from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import cost_centers as constants


@admin.register(models.CostCenter)
class CostCenterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "accounting_id", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
