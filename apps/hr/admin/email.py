from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models


@admin.register(models.Email)
class EmailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "email", "fullname")
    list_display_links = ("id", "email")
    search_fields = (
        "employee__firstname",
        "employee__father_name",
        "employee__lastname",
        "email",
    )
    autocomplete_fields = ("employee",)
    list_per_page = 20

    @admin.display(description="Fullname")
    def fullname(self, obj: models.Email):
        return f"{obj.employee.firstname} {obj.employee.father_name} {obj.employee.lastname}"
