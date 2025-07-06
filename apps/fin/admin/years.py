from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import years as constants


@admin.register(models.Year)
class YearAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (("name", "description"),)
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.YearResource,)
