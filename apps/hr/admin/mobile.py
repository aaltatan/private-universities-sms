from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from import_export.admin import ImportExportModelAdmin

from .. import models, resources


@admin.register(models.Mobile)
class MobileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "number", "has_whatsapp", "employee__fullname")
    list_display_links = ("id", "number")
    search_fields = ("employee__fullname", "number")
    autocomplete_fields = ("employee",)
    list_per_page = 20
    actions = ("remove_whatsapp", "add_whatsapp")
    resource_classes = (resources.MobileResource,)

    @admin.action(description="Remove has_whatsapp from selected Mobiles")
    def remove_whatsapp(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(has_whatsapp=False)
        self.message_user(
            request,
            "Has whatsapp has been removed from selected mobiles",
        )

    @admin.action(description="Add has_whatsapp from selected Mobiles")
    def add_whatsapp(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(has_whatsapp=True)
        self.message_user(
            request,
            "Has whatsapp has been added to selected mobiles",
        )
