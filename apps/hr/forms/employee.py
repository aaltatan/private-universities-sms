from datetime import datetime

from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.models import User
from apps.core.utils import calculate_age_in_years
from apps.core.widgets import (
    AvatarWidget,
    SelectMultipleWidget,
    get_date_widget,
    get_input_datalist,
    get_numeric_widget,
    get_text_widget,
    get_textarea_widget,
)
from apps.edu.models import School, Specialization
from apps.geo.models import City, Nationality
from apps.org.models import Group, Position

from .. import models


class EmployeeForm(forms.ModelForm):
    city = get_autocomplete_field(
        City.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search cities")},
        app_label="geo",
        model_name="City",
        object_name="city",
        field_name="search",
    )
    nationality = get_autocomplete_field(
        Nationality.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search nationalities")},
        app_label="geo",
        model_name="Nationality",
        object_name="nationality",
        field_name="search",
    )
    position = get_autocomplete_field(
        Position.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search positions")},
        app_label="org",
        model_name="Position",
        object_name="position",
        field_name="search",
    )
    school = get_autocomplete_field(
        School.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search schools")},
        app_label="edu",
        model_name="School",
        object_name="school",
        field_name="search",
    )
    specialization = get_autocomplete_field(
        Specialization.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search specializations")},
        app_label="edu",
        model_name="Specialization",
        object_name="specialization",
        field_name="search",
    )
    user = get_autocomplete_field(
        User.objects.all(),
        to_field_name="username",
        widget_attributes={"placeholder": _("search users")},
        app_label="core",
        model_name="User",
        object_name="user",
        field_name="username",
        field_attributes={"required": False},
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=SelectMultipleWidget,
        required=False,
    )
    profile = forms.ImageField(
        required=False,
        widget=AvatarWidget(attrs={"accept": "image/*"}),
    )

    def clean_birth_date(self):
        birth_date: datetime = self.cleaned_data.get("birth_date")
        age: int = calculate_age_in_years(birth_date)
        min_age = settings.MIN_EMPLOYEE_AGE

        if timezone.now().date() < birth_date:
            self.add_error(
                "birth_date",
                _("birth date cannot be in the future"),
            )

        if age < min_age:
            self.add_error(
                "birth_date",
                _("employee's age must be at least {} years old").format(min_age),
            )

        return birth_date

    def clean_hire_date(self):
        hire_date = self.cleaned_data.get("hire_date")
        if timezone.now().date() < hire_date:
            self.add_error(
                "hire_date",
                _("hire date cannot be in the future"),
            )
        return hire_date

    def clean_card_date(self):
        card_date = self.cleaned_data.get("card_date")
        if timezone.now().date() < card_date:
            self.add_error(
                "card_date",
                _("card date cannot be in the future"),
            )
        return card_date

    class Meta:
        model = models.Employee
        exclude = ("slug", "ordering")
        widgets = {
            "firstname": get_text_widget(placeholder=_("first name").title()),
            "lastname": get_text_widget(placeholder=_("last name").title()),
            "father_name": get_text_widget(
                placeholder=_("father name").title(),
            ),
            "mother_name": get_text_widget(
                placeholder=_("mother name").title(),
            ),
            "birth_place": get_text_widget(
                placeholder=_("birth place").title(),
            ),
            "birth_date": get_date_widget(
                placeholder=_("birth date").title(),
            ),
            "national_id": get_numeric_widget(
                x_mask="9" * 12,
                placeholder=_("national id").title(),
            ),
            "passport_id": get_numeric_widget(
                placeholder=_("passport id").title(),
            ),
            "card_id": get_numeric_widget(
                placeholder=_("card id").title(),
            ),
            "civil_registry_office": get_input_datalist(
                model=models.Employee,
                field_name="civil_registry_office",
                placeholder=_("civil registry office").title(),
            ),
            "registry_office_name": get_input_datalist(
                model=models.Employee,
                field_name="registry_office_name",
                placeholder=_("registry office name").title(),
            ),
            "registry_office_id": get_numeric_widget(
                placeholder=_("registry office id").title()
            ),
            "face_color": get_input_datalist(
                model=models.Employee,
                field_name="face_color",
                placeholder=_("face color").title(),
            ),
            "eyes_color": get_input_datalist(
                model=models.Employee,
                field_name="eyes_color",
                placeholder=_("eyes color").title(),
            ),
            "address": get_text_widget(
                placeholder=_("address").title(),
            ),
            "current_address": get_text_widget(
                placeholder=_("current address").title()
            ),
            "special_signs": get_textarea_widget(
                placeholder=_("special signs").title()
            ),
            "card_date": get_date_widget(placeholder=_("card date").title()),
            "hire_date": get_date_widget(placeholder=_("hire date").title()),
            "notes": get_textarea_widget(placeholder=_("notes").title()),
        }
