from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import Activity, User
from .utils import dict_to_css

admin.site.register(User, UserAdmin)


@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    @admin.display(description="Kind")
    def formatted_kind(self, obj: Activity) -> str:
        colors = {
            "create": "green",
            "update": "orangered",
            "delete": "red",
            "export": "blue",
        }
        styles = {
            "color": "white",
            "border-radius": "0.25rem",
            "padding": "0.125rem 0.25rem",
            "font-size": "0.75rem",
            "text-transform": "capitalize",
        }
        styles["background-color"] = colors[obj.kind]
        return format_html(
            f'<div style="{dict_to_css(styles)}">{obj.kind}</div>',
        )

    list_per_page = 20
    list_display = (
        "created_at",
        "user",
        "formatted_kind",
        "content_type",
        "content_object",
        "object_id",
        "notes",
    )
    search_fields = (
        "user__username",
        "notes",
    )
    list_filter = (
        "user__username",
        "content_type",
        "kind",
    )
    readonly_fields = (
        "created_at",
        "user",
        "kind",
        "data",
        "content_type",
        "object_id",
    )
