from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import employee as constants


class MobileInline(admin.TabularInline):
    model = models.Mobile
    extra = 1
    fields = ("number", "kind", "has_whatsapp")


class EmailInline(admin.TabularInline):
    model = models.Email
    extra = 1
    fields = ("email", "kind")


class PhoneInline(admin.TabularInline):
    model = models.Phone
    extra = 1
    fields = ("number", "kind")


@admin.register(models.Employee)
class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "fullname",
        "gender",
        "city__name",
        "cost_center__name",
        "position__name",
        "job_subtype__name",
        "job_subtype__job_type__name",
        "degree__name",
        "specialization__name",
    )
    search_fields = constants.SEARCH_FIELDS
    fields = (
        ("profile",),
        ("firstname", "lastname", "father_name", "mother_name"),
        ("birth_place", "birth_date"),
        ("national_id", "passport_id", "nationality"),
        ("card_id"),
        ("civil_registry_office"),
        ("registry_office_name", "registry_office_id"),
        ("gender", "face_color", "eyes_color"),
        ("address", "current_address", "city"),
        ("special_signs",),
        ("card_date",),
        ("martial_status", "military_status", "religion"),
        ("hire_date",),
        ("notes",),
        ("cost_center", "position", "status", "job_subtype"),
        ("groups",),
        ("degree", "school", "specialization"),
        ("user",),
    )
    autocomplete_fields = (
        "nationality",
        "city",
        "cost_center",
        "position",
        "status",
        "job_subtype",
        "degree",
        "school",
        "specialization",
        "user",
    )
    filter_horizontal = ("groups",)
    list_filter = (
        "nationality__name",
        "cost_center__name",
        "position__name",
        "status__name",
        "job_subtype__name",
        "degree__name",
        "school__kind__name",
        "specialization__name",
        "specialization__is_specialist",
    )
    list_per_page = 20
    inlines = (MobileInline, PhoneInline, EmailInline)

    @admin.display(description="Fullname")
    def fullname(self, obj: models.Employee):
        return f"{obj.firstname} {obj.father_name} {obj.lastname}"
