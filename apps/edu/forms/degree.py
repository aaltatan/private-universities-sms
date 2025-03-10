from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets

from .. import models


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
