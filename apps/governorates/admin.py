from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.cities.models import City

from . import constants, models


class TabularCity(admin.TabularInline):
    model = City
    fields = ("name",)
    extra = 0


@admin.register(models.Governorate)
class GovernorateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    inlines = (TabularCity,)
