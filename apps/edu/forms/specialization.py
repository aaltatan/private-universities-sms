from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core import widgets
from apps.core.forms import CustomModelForm

from .. import models


class SpecializationForm(CustomModelForm):
    is_specialist = forms.ChoiceField(
        choices=models.Specialization.SpecialistChoices,
        label=_("is specialist"),
        initial=models.Specialization.SpecialistChoices.SPECIALIST,
    )

    class Meta:
        model = models.Specialization
        fields = ("name", "is_specialist", "description")
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("e.g. Computer Science")),
            "description": widgets.get_textarea_widget(placeholder=_("some description")),
        }
