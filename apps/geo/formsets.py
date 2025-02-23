from django.forms import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from . import forms, models


class CustomFormset(BaseInlineFormSet):
    def clean(self):
        lens: int = 0

        for item in self.cleaned_data:
            lens += len(item.get("name", ""))

        if lens > 100:
            raise ValidationError(
                "total cities names letters count's must be less than 100 characters",
            )

        super().clean()


CityFormset = inlineformset_factory(
    parent_model=models.Governorate,
    model=models.City,
    form=forms.CityForm,
    formset=CustomFormset,
    can_delete=True,
    extra=1,
    fields=("name",),
)
