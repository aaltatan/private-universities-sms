from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import job_types as constants


class JobSubtypeInline(admin.TabularInline):
    model = models.JobSubtype
    fields = ("name",)
    extra = 0


@admin.register(models.JobType)
class JobTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = (("name", "description"),)
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    inlines = (JobSubtypeInline,)
    resource_classes = (resources.JobTypeResource,)
