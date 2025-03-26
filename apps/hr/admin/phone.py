from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources


@admin.register(models.Phone)
class PhoneAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "number", "fullname")
    list_display_links = ("id", "number")
    autocomplete_fields = ("employee",)
    list_per_page = 20
    search_fields = (
        "employee__firstname",
        "employee__father_name",
        "employee__lastname",
        "number",
    )
    resource_classes = (resources.PhoneResource,)

    @admin.display(description="Fullname")
    def fullname(self, obj: models.Phone):
        return obj.employee.get_fullname()
