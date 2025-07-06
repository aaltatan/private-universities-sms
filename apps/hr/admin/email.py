from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources


@admin.register(models.Email)
class EmailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = ("email", "employee", "notes")
    list_display = ("id", "email", "employee__fullname")
    list_display_links = ("id", "email")
    search_fields = ("employee__fullname", "email")
    autocomplete_fields = ("employee",)
    list_per_page = 20
    resource_classes = (resources.EmailResource,)
