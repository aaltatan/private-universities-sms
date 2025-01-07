from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.core.admin import CustomDjangoQLSearchMixin

from . import models, constants


@admin.register(models.Governorate)
class GovernorateAdmin(
    CustomDjangoQLSearchMixin,
    ImportExportModelAdmin,
    admin.ModelAdmin,
):
    list_display = ("id", "name", "slug")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
