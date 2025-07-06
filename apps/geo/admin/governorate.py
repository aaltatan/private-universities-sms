from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import governorates as constants


class TabularCity(admin.TabularInline):
    model = models.City
    fields = ("name",)
    extra = 0


@admin.register(models.Governorate)
class GovernorateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (("name", "description"),)
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    inlines = (TabularCity,)
    resource_classes = (resources.GovernorateResource,)
