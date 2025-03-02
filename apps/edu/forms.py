from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.fields import get_autocomplete_field
from apps.geo.models import Nationality

from . import models


class SchoolForm(forms.ModelForm):
    nationality = get_autocomplete_field(
        queryset=Nationality.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search nationalities")},
        app_label="geo",
        model_name="Nationality",
        object_name="nationality",
        field_name="search",
    )
    kind = get_autocomplete_field(
        queryset=models.SchoolKind.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search school kinds")},
        app_label="edu",
        model_name="Schoolkind",
        object_name="schoolkind",
        field_name="search",
    )

    class Meta:
        model = models.School
        fields = (
            "name",
            "kind",
            "nationality",
            "website",
            "email",
            "phone",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("school name")),
            "description": widgets.get_textarea_widget(),
            "email": widgets.get_email_widget(),
            "website": widgets.get_url_widget(),
            "phone": widgets.get_text_widget(
                placeholder=_("phone number").title(),
            ),
        }


class SchoolKindForm(forms.ModelForm):
    is_governmental = forms.ChoiceField(
        choices=models.SchoolKind.OwnershipChoices,
        label=_("is governmental"),
        initial=models.SchoolKind.OwnershipChoices.GOVERNMENTAL,
        help_text=_("is it governmental or private"),
    )
    is_virtual = forms.ChoiceField(
        choices=models.SchoolKind.VirtualChoices,
        label=_("is virtual"),
        initial=models.SchoolKind.VirtualChoices.ORDINARY,
        help_text=_("is it virtual or ordinary"),
    )

    class Meta:
        model = models.SchoolKind
        fields = (
            "name",
            "is_governmental",
            "is_virtual",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("school kind name")),
            "description": widgets.get_textarea_widget(),
        }


class SpecializationForm(forms.ModelForm):
    is_specialist = forms.ChoiceField(
        choices=models.Specialization.SpecialistChoices,
        label=_("is governmental"),
        initial=models.Specialization.SpecialistChoices.SPECIALIST,
        help_text=_("is it governmental or private"),
    )

    class Meta:
        model = models.Specialization
        fields = ("name", "is_specialist", "description")
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("specialization name")),
            "description": widgets.get_textarea_widget(),
        }


class DegreeForm(forms.ModelForm):
    is_academic = forms.ChoiceField(
        choices=models.Degree.AcademicChoices,
        label=_("is academic"),
        initial=models.Degree.AcademicChoices.ACADEMIC,
        help_text=_("is it academic or applied"),
    )

    class Meta:
        model = models.Degree
        fields = ("name", "order", "is_academic", "description")
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("degree name")),
            "description": widgets.get_textarea_widget(),
        }
