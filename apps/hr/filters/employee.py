import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterComboboxMixin,
    FilterTextMixin,
    get_combobox_choices_filter,
    get_date_from_to_filters,
    get_number_from_to_filters,
    get_text_filter,
)
from apps.edu.models import Degree, Specialization
from apps.geo.models import Nationality
from apps.org.models import Status

from .. import choices, models
from ..managers import EmployeeQuerySet


class GroupedByCountFilter(filters.FilterSet):
    group_by = filters.TypedChoiceFilter(
        label=_("group by").title(),
        choices=choices.CountsGroupedByChoices,
        method="filter_counts_grouped_by",
    )

    def filter_counts_grouped_by(self, queryset: EmployeeQuerySet, name, value):
        return queryset.get_counts_grouped_by(group_by=value)

    class Meta:
        model = models.Employee
        fields = ("group_by",)


class UpcomingBirthdayFilter(filters.FilterSet):
    this = filters.TypedChoiceFilter(
        label=_("this").title(),
        choices=choices.DateUnitsChoices,
        method="filter_upcoming_birthday_this",
    )

    def filter_upcoming_birthday_this(self, queryset: EmployeeQuerySet, name, value):
        return queryset.get_upcoming_birthdays(this=value)

    class Meta:
        model = models.Employee
        fields = ("this",)


class UpcomingJobAnniversaryFilter(filters.FilterSet):
    this = filters.TypedChoiceFilter(
        label=_("this").title(),
        choices=choices.DateUnitsChoices,
        method="filter_upcoming_job_anniversary_this",
    )

    def filter_upcoming_job_anniversary_this(
        self, queryset: EmployeeQuerySet, name, value
    ):
        return queryset.get_upcoming_job_anniversaries(this=value)

    class Meta:
        model = models.Employee
        fields = ("this",)


class BaseEmployeeFilter(
    FilterComboboxMixin,
    FilterTextMixin,
    filters.FilterSet,
):
    firstname = get_text_filter(label=_("first name").title())
    lastname = get_text_filter(label=_("last name").title())
    father_name = get_text_filter(label=_("father name").title())
    mother_name = get_text_filter(label=_("mother name").title())
    birth_place = get_text_filter(label=_("birth place").title())
    birth_date_from, birth_date_to = get_date_from_to_filters(
        field_name="birth_date",
    )
    age_from, age_to = get_number_from_to_filters(
        field_name="age",
    )
    age_group = filters.ChoiceFilter(
        field_name="age_group",
        label=_("age group").title(),
        choices=choices.AgeGroupChoices,
    )
    national_id = get_text_filter(label=_("national id").title())
    card_id = get_text_filter(label=_("card id").title())
    passport_id = get_text_filter(label=_("passport id").title())
    civil_registry_office = get_text_filter(
        label=_("civil registry office").title(),
    )
    registry_office_name = get_text_filter(
        label=_("registry office name").title(),
    )
    registry_office_id = get_text_filter(label=_("registry office id").title())
    address = get_text_filter(label=_("address").title())
    special_signs = get_text_filter(label=_("special signs").title())
    card_date_from, card_date_to = get_date_from_to_filters(
        field_name="card_date",
    )
    current_address = get_text_filter(label=_("current address").title())
    hire_date_from, hire_date_to = get_date_from_to_filters(
        field_name="hire_date",
    )
    job_age_from, job_age_to = get_number_from_to_filters(
        field_name="job_age",
    )
    notes = get_text_filter(label=_("notes").title())
    is_specialist = filters.ChoiceFilter(
        field_name="specialization__is_specialist",
        label=_("specialty").title(),
        choices=Specialization.SpecialistChoices,
    )
    is_academic = filters.ChoiceFilter(
        field_name="degree__is_academic",
        label=_("academic").title(),
        choices=Degree.AcademicChoices,
    )
    is_payable = filters.ChoiceFilter(
        field_name="status__is_payable",
        label=_("payability").title(),
        choices=Status.PayableChoices,
    )
    is_local = filters.ChoiceFilter(
        field_name="nationality__is_local",
        label=_("locality").title(),
        choices=Nationality.LocalityChoices,
    )
    upcoming_birthday_this = filters.ChoiceFilter(
        label=_("upcoming birthday this").title(),
        choices=choices.DateUnitsChoices,
        method="filter_upcoming_birthday_this",
    )
    upcoming_job_anniversary_this = filters.ChoiceFilter(
        label=_("upcoming job anniversary this").title(),
        choices=choices.DateUnitsChoices,
        method="filter_upcoming_job_anniversary_this",
    )

    def filter_upcoming_birthday_this(self, queryset: EmployeeQuerySet, name, value):
        return queryset.get_upcoming_birthdays(this=value)

    def filter_upcoming_job_anniversary_this(
        self, queryset: EmployeeQuerySet, name, value
    ):
        return queryset.get_upcoming_job_anniversaries(this=value)

    class Meta:
        model = models.Employee
        exclude = (
            "id",
            "slug",
            "ordering",
            "user",
            "profile",
            "identity_document",
        )


class APIEmployeeFilter(BaseEmployeeFilter):
    face_color = get_combobox_choices_filter(
        model=models.Employee,
        field_name="face_color",
        label=_("face color"),
        api_filter=True,
    )
    eyes_color = get_combobox_choices_filter(
        model=models.Employee,
        field_name="eyes_color",
        label=_("eyes color"),
        api_filter=True,
    )
    martial_status = get_combobox_choices_filter(
        model=models.Employee,
        field_name="martial_status",
        label=_("martial status"),
        choices=models.Employee.MartialStatusChoices.choices,
        api_filter=True,
    )
    military_status = get_combobox_choices_filter(
        model=models.Employee,
        field_name="military_status",
        label=_("military status"),
        choices=models.Employee.MilitaryStatus.choices,
        api_filter=True,
    )
    religion = get_combobox_choices_filter(
        model=models.Employee,
        field_name="religion",
        label=_("religion"),
        choices=models.Employee.ReligionChoices.choices,
        api_filter=True,
    )
    nationality = get_combobox_choices_filter(
        model=models.Employee,
        field_name="nationality__name",
        label=_("nationality"),
        api_filter=True,
    )
    governorate = get_combobox_choices_filter(
        model=models.Employee,
        field_name="city__governorate__name",
        label=_("governorate"),
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
    job_type = get_combobox_choices_filter(
        model=models.Employee,
        field_name="job_subtype__job_type__name",
        label=_("job type"),
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
    groups_combined = get_combobox_choices_filter(
        model=models.Employee,
        field_name="groups__name",
        method_name="filter_combobox_combined",
        label=_("groups combined"),
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
    school_kind = get_combobox_choices_filter(
        model=models.Employee,
        field_name="school__kind__name",
        label=_("school kind"),
        api_filter=True,
    )
    specialization = get_combobox_choices_filter(
        model=models.Employee,
        field_name="specialization__name",
        label=_("specialization"),
        api_filter=True,
    )


class EmployeeFilter(BaseEmployeeFilter):
    face_color = get_combobox_choices_filter(
        model=models.Employee,
        field_name="face_color",
        label=_("face color"),
    )
    eyes_color = get_combobox_choices_filter(
        model=models.Employee,
        field_name="eyes_color",
        label=_("eyes color"),
    )
    martial_status = get_combobox_choices_filter(
        model=models.Employee,
        field_name="martial_status",
        label=_("martial status"),
        choices=models.Employee.MartialStatusChoices.choices,
    )
    military_status = get_combobox_choices_filter(
        model=models.Employee,
        field_name="military_status",
        label=_("military status"),
        choices=models.Employee.MilitaryStatus.choices,
    )
    religion = get_combobox_choices_filter(
        model=models.Employee,
        field_name="religion",
        label=_("religion"),
        choices=models.Employee.ReligionChoices.choices,
    )
    nationality = get_combobox_choices_filter(
        model=models.Employee,
        field_name="nationality__name",
        label=_("nationality"),
    )
    governorate = get_combobox_choices_filter(
        model=models.Employee,
        field_name="city__governorate__name",
        label=_("governorate"),
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
    job_type = get_combobox_choices_filter(
        model=models.Employee,
        field_name="job_subtype__job_type__name",
        label=_("job type"),
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
    groups_combined = get_combobox_choices_filter(
        model=models.Employee,
        field_name="groups__name",
        method_name="filter_combobox_combined",
        label=_("groups combined"),
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
    school_kind = get_combobox_choices_filter(
        model=models.Employee,
        field_name="school__kind__name",
        label=_("school kind"),
    )
    specialization = get_combobox_choices_filter(
        model=models.Employee,
        field_name="specialization__name",
        label=_("specialization"),
    )
