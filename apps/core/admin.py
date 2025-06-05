from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .models import Activity, User
from .utils import badge_component

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
        return badge_component(background_color=colors[obj.kind], text=obj.kind)

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


admin.site.site_header = "Private Universities Salaries Management System"
admin.site.site_title = "PUSMS"
admin.site.index_title = "PUSMS"
