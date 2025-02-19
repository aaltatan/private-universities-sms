from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_textarea_widget, get_text_widget
from apps.core.fields import get_autocomplete_field

from . import models


class GovernorateForm(forms.ModelForm):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("governorate name")),
            "description": get_textarea_widget(),
        }


class CityForm(forms.ModelForm):
    governorate = get_autocomplete_field(
        queryset=models.Governorate.objects.all(),
        to_field_name="name",
        attributes={"placeholder": _("search governorates")},
        app_label="geo",
        model_name="Governorate",
        object_name="governorate",
        field_name="search",
    )

    class Meta:
        model = models.City
        fields = ("name", "governorate", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("city name")),
            "description": get_textarea_widget(),
        }


class NationalityForm(forms.ModelForm):
    is_local = forms.ChoiceField(
        choices=models.Nationality.LocalityChoices,
        label=_("locality"),
        help_text=_("is it local or foreign"),
    )

    class Meta:
        model = models.Nationality
        fields = ("name", "is_local", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("nationality name")),
            "description": get_textarea_widget(),
        }
