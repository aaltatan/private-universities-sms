from django import forms
from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseCityForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = ("name", "governorate", "kind", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("city name")),
            "description": get_textarea_widget(),
        }


class CityForm(BaseCityForm):
    governorate = get_autocomplete_field(
        queryset=models.Governorate.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search governorates")},
        app_label="geo",
        model_name="Governorate",
        object_name="governorate",
        field_name="search",
    )
