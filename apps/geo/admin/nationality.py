from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import nationalities


@admin.register(models.Nationality)
class NationalityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (("name", "is_local", "description"),)
    list_display = ("id", "name", "is_local", "slug")
    list_display_links = ("id", "name")
    search_fields = nationalities.SEARCH_FIELDS
    list_per_page = 20
    resource_classes = (resources.NationalityResource,)
