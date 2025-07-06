from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import job_types as constants


class TabularEmployee(admin.TabularInline):
    model = models.Group.employees.through
    extra = 0
    autocomplete_fields = ("employee",)


@admin.register(models.Group)
class GroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (
        ("name", "kind"),
        "description",
    )
    list_display = ("id", "name", "kind", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.GroupResource,)
    inlines = (TabularEmployee,)
