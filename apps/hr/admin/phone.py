from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources


@admin.register(models.Phone)
class PhoneAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = ("number", "employee", "notes")
    list_display = ("id", "number", "employee__fullname")
    list_display_links = ("id", "number")
    autocomplete_fields = ("employee",)
    list_per_page = 20
    search_fields = (
        "employee__fullname",
        "number",
    )
    resource_classes = (resources.PhoneResource,)
