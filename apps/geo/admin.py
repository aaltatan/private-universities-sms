from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models
from .constants import cities, governorates


class TabularCity(admin.TabularInline):
    model = models.City
    fields = ("name",)
    extra = 0


@admin.register(models.Governorate)
class GovernorateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = governorates.SEARCH_FIELDS
    list_per_page = 20
    inlines = (TabularCity,)


@admin.register(models.City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "governorate__name", "description")
    list_display_links = ("id", "name")
    search_fields = cities.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("governorate",)
