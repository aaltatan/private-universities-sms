from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets

from .. import models


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
