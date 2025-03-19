import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseQSearchFilter,
    get_ordering_filter,
    get_date_from_to_filters,
    get_combobox_choices_filter,
)

from .. import models
from ..constants import employee as constants


class BaseEmployeeFilter(filters.FilterSet):
    birth_date_from, birth_date_to = get_date_from_to_filters(
        field_name="birth_date",
    )
    card_date_from, card_date_to = get_date_from_to_filters(
        field_name="card_date",
    )
    hire_date_from, hire_date_to = get_date_from_to_filters(
        field_name="hire_date",
    )

    class Meta:
        model = models.Employee
        fields = (
            "firstname",
            "lastname",
            "father_name",
            "mother_name",
            "birth_place",
            "birth_date_from",
            "birth_date_to",
            "national_id",
            "passport_id",
            "card_id",
            "civil_registry_office",
            "registry_office_name",
            "registry_office_id",
            "gender",
            "face_color",
            "eyes_color",
            "address",
            "special_signs",
            "card_date_from",
            "card_date_to",
            "martial_status",
            "military_status",
            "religion",
            "current_address",
            "nationality",
            "city",
            "hire_date_from",
            "hire_date_to",
            "notes",
            "cost_center",
            "position",
            "status",
            "job_subtype",
            "groups",
            "degree",
            "school",
            "specialization",
            "user",
        )


class APIEmployeeFilter(BaseEmployeeFilter):
    nationality = get_combobox_choices_filter(
        model=models.Employee,
        field_name="nationality__name",
        label=_("nationality"),
        api_filter=True,
    )
    city = get_combobox_choices_filter(
        model=models.Employee,
        field_name="city__name",
        label=_("city"),
        api_filter=True,
    )
    cost_center = get_combobox_choices_filter(
        model=models.Employee,
        field_name="cost_center__name",
        label=_("cost center"),
        api_filter=True,
    )
    position = get_combobox_choices_filter(
        model=models.Employee,
        field_name="position__name",
        label=_("position"),
        api_filter=True,
    )
    status = get_combobox_choices_filter(
        model=models.Employee,
        field_name="status__name",
        label=_("status"),
        api_filter=True,
    )
    job_subtype = get_combobox_choices_filter(
        model=models.Employee,
        field_name="job_subtype__name",
        label=_("job subtype"),
        api_filter=True,
    )
    groups = get_combobox_choices_filter(
        model=models.Employee,
        field_name="groups__name",
        label=_("groups"),
        api_filter=True,
    )
    degree = get_combobox_choices_filter(
        model=models.Employee,
        field_name="degree__name",
        label=_("degree"),
        api_filter=True,
    )
    school = get_combobox_choices_filter(
        model=models.Employee,
        field_name="school__name",
        label=_("school"),
        api_filter=True,
    )
    specialization = get_combobox_choices_filter(
        model=models.Employee,
        field_name="specialization__name",
        label=_("specialization"),
        api_filter=True,
    )
    user = get_combobox_choices_filter(
        model=models.Employee,
        field_name="user__username",
        label=_("user"),
        api_filter=True,
    )


class EmployeeFilter(BaseQSearchFilter, BaseEmployeeFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    nationality = get_combobox_choices_filter(
        model=models.Employee,
        field_name="nationality__name",
        label=_("nationality"),
    )
    city = get_combobox_choices_filter(
        model=models.Employee,
        field_name="city__name",
        label=_("city"),
    )
    cost_center = get_combobox_choices_filter(
        model=models.Employee,
        field_name="cost_center__name",
        label=_("cost center"),
    )
    position = get_combobox_choices_filter(
        model=models.Employee,
        field_name="position__name",
        label=_("position"),
    )
    status = get_combobox_choices_filter(
        model=models.Employee,
        field_name="status__name",
        label=_("status"),
    )
    job_subtype = get_combobox_choices_filter(
        model=models.Employee,
        field_name="job_subtype__name",
        label=_("job subtype"),
    )
    groups = get_combobox_choices_filter(
        model=models.Employee,
        field_name="groups__name",
        label=_("groups"),
    )
    degree = get_combobox_choices_filter(
        model=models.Employee,
        field_name="degree__name",
        label=_("degree"),
    )
    school = get_combobox_choices_filter(
        model=models.Employee,
        field_name="school__name",
        label=_("school"),
    )
    specialization = get_combobox_choices_filter(
        model=models.Employee,
        field_name="specialization__name",
        label=_("specialization"),
    )
    user = get_combobox_choices_filter(
        model=models.Employee,
        field_name="user__username",
        label=_("user"),
    )
