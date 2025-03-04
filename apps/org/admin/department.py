from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from ..constants import departments as constants
from ..models import Department


@admin.register(Department)
class DepartmentAdmin(TreeAdmin):
    list_display = (
        "name",
        "cost_center__name",
        "description",
    )
    list_display_links = ("name",)
    search_fields = constants.SEARCH_FIELDS
    list_per_page = 200
    autocomplete_fields = ("cost_center",)
    form = movenodeform_factory(Department)