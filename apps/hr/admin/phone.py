from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models


@admin.register(models.Phone)
class PhoneAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("fullname", "number")
    autocomplete_fields = ("employee",)
    list_per_page = 20
    search_fields = (
        "employee__firstname",
        "employee__father_name",
        "employee__lastname",
        "number",
    )

    @admin.display(description="Fullname")
    def fullname(self, obj: models.Phone):
        return f"{obj.employee.firstname} {obj.employee.father_name} {obj.employee.lastname}"
