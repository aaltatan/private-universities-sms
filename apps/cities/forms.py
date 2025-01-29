from django import forms

from apps.core.widgets import get_autocomplete_field

from .models import City, Governorate


class CityForm(forms.ModelForm):
    governorate = get_autocomplete_field(
        queryset=Governorate.objects.all(),
        app_label="governorates",
        model_name="Governorate",
        object_name="governorate",
        field_name="name",
    )

    class Meta:
        model = City
        fields = ("name", "governorate", "description")
