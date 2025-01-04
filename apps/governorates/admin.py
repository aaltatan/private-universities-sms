from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.core.admin import CustomDjangoQLSearchMixin

from . import models


@admin.register(models.Governorate)
class GovernorateAdmin(
    CustomDjangoQLSearchMixin,
    ImportExportModelAdmin,
    admin.ModelAdmin,
):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    list_per_page = 20
