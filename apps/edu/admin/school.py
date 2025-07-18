from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import schools as constants


@admin.register(models.School)
class SchoolAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        "name",
        ("nationality", "kind"),
        ("website", "email", "phone", "address"),
        "description",
    )
    list_display = (
        "id",
        "name",
        "kind__name",
        "nationality__name",
        "description",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("nationality", "kind")
    resource_classes = (resources.SchoolResource,)
