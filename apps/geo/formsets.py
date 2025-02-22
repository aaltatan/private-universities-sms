from django.forms.models import inlineformset_factory

from . import forms, models


CityFormset = inlineformset_factory(
    parent_model=models.Governorate,
    model=models.City,
    form=forms.CityForm,
    can_delete=True,
    extra=1,
    fields=("name",),
)
