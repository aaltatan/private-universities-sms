from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from import_export.admin import ImportExportModelAdmin

from .. import models, resources
from ..constants import job_subtypes as constants


@admin.register(models.JobSubtype)
class JobSubtypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "job_type__name", "ordering", "slug")
    list_display_links = ("id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("job_type",)
    list_filter = ("job_type__name",)
    actions = ("reset_ordering",)
    resource_classes = (resources.JobSubtypeResource,)

    @admin.action(description="Reset ordering for selected Job Subtypes")
    def reset_ordering(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(ordering=0)
        self.message_user(
            request,
            "Ordering for selected job subtypes has been reset",
        )
