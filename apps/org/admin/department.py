from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from ..constants import departments as constants
from ..models import Department


@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin):
    list_display = (
        "tree_actions",
        "indented_title",
        "tree_id",
        "name",
        "parent__name",
        "cost_center__name",
        "description",
    )
    list_display_links = ("indented_title", "tree_id", "name")
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 20
    autocomplete_fields = ("cost_center", "parent")
    mptt_indent_field = "name"
    mptt_level_indent = 24
