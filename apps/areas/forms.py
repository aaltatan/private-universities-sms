from django import forms

from apps.core.widgets import get_autocomplete_field

from .models import City, Governorate


class GovernorateForm(forms.ModelForm):
    class Meta:
        model = Governorate
        fields = ("name", "description")


class CityForm(forms.ModelForm):
    governorate = get_autocomplete_field(
        queryset=Governorate.objects.all(),
        to_field_name="name",
        app_label="areas",
        model_name="Governorate",
        object_name="governorate",
        field_name="search",
    )

    class Meta:
        model = City
        fields = ("name", "governorate", "description")
