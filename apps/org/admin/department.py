from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from ..constants import departments as constants
from ..models import Department


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    list_display = (
        "name",
        "parent__name",
        "level",
        "cost_center__name",
        "description",
    )
    list_display_links = ("name",)
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 200
    autocomplete_fields = ("cost_center", "parent")
    mptt_indent_field = "name"
    mptt_level_indent = 24
