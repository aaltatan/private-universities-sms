from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import school_kinds as constants


@admin.register(models.SchoolKind)
class SchoolKindAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        ("name", "is_governmental", "is_virtual"),
        "description",
    )
    list_display = (
        "id",
        "name",
        "is_governmental",
        "is_virtual",
        "description",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.SchoolKindResource,)
