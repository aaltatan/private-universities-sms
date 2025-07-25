from django import forms
from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.forms import CustomModelForm
from apps.core.models import User
from apps.core.widgets import (
    AvatarWidget,
    SelectMultipleWidget,
    get_date_widget,
    get_file_widget,
    get_input_datalist_widget,
    get_numeric_widget,
    get_text_widget,
    get_textarea_widget,
)
from apps.edu.models import Degree, School, Specialization
from apps.geo.models import City, Nationality
from apps.org.models import CostCenter, Group, JobSubtype, Position, Status

from .. import models


class EmployeeForm(CustomModelForm):
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
    cost_center = get_autocomplete_field(
        CostCenter.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search cost centers")},
        app_label="org",
        model_name="CostCenter",
        object_name="cost_center",
        field_name="search",
    )
    job_subtype = get_autocomplete_field(
        JobSubtype.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search job subtypes")},
        app_label="org",
        model_name="JobSubtype",
        object_name="job_subtype",
        field_name="search",
    )
    status = get_autocomplete_field(
        Status.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search statuses")},
        app_label="org",
        model_name="Status",
        object_name="status",
        field_name="search",
    )
    degree = get_autocomplete_field(
        Degree.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search degrees")},
        app_label="edu",
        model_name="Degree",
        object_name="degree",
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
        User.objects.filter(is_active=True, is_staff=False),
        to_field_name="username",
        widget_attributes={"placeholder": _("search users")},
        queryset_filters={"is_active": True, "is_staff": False},
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
        widget=AvatarWidget(
            attrs={
                "accept": ".jpg,.jpeg,.png",
            }
        ),
    )

    class Meta:
        model = models.Employee
        exclude = ("slug", "ordering")
        widgets = {
            "firstname": get_text_widget(placeholder=_("e.g. John")),
            "lastname": get_text_widget(placeholder=_("e.g. Doe")),
            "father_name": get_text_widget(placeholder=_("e.g. John")),
            "mother_name": get_text_widget(placeholder=_("e.g. Jane")),
            "birth_place": get_input_datalist_widget(
                model=models.Employee,
                field_name="birth_place",
                placeholder=_("e.g. Hama"),
            ),
            "birth_date": get_date_widget(placeholder=_("e.g. 1990-01-01")),
            "national_id": get_numeric_widget(
                x_mask="9" * 12,
                placeholder="0123456789",
            ),
            "passport_id": get_numeric_widget(placeholder="0123456789"),
            "card_id": get_numeric_widget(placeholder="0123456789"),
            "civil_registry_office": get_input_datalist_widget(
                model=models.Employee,
                field_name="civil_registry_office",
                placeholder=_("e.g. Cairo"),
            ),
            "registry_office_name": get_input_datalist_widget(
                model=models.Employee,
                field_name="registry_office_name",
                placeholder=_("e.g. Cairo"),
            ),
            "registry_office_id": get_numeric_widget(placeholder="3123"),
            "face_color": get_input_datalist_widget(
                model=models.Employee,
                field_name="face_color",
                placeholder=_("e.g. White"),
            ),
            "eyes_color": get_input_datalist_widget(
                model=models.Employee,
                field_name="eyes_color",
                placeholder=_("e.g. Blue"),
            ),
            "address": get_text_widget(
                placeholder=_("e.g. 123 Main Street, Cairo"),
            ),
            "current_address": get_text_widget(
                placeholder=_("e.g. 123 Main Street, Cairo"),
            ),
            "special_signs": get_input_datalist_widget(
                model=models.Employee,
                field_name="special_signs",
                placeholder=_("e.g. Glasses"),
            ),
            "card_date": get_date_widget(placeholder=_("e.g. 2022-01-01")),
            "hire_date": get_date_widget(placeholder=_("e.g. 2022-01-01")),
            "separation_date": get_date_widget(
                placeholder=_("e.g. 2022-01-01"), fill_onfocus=False
            ),
            "notes": get_textarea_widget(placeholder=_("some notes")),
            "identity_document": get_file_widget(),
        }
