from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import degrees as constants


@admin.register(models.Degree)
class DegreeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "order",
        "is_academic",
        "description",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.DegreeResource,)
