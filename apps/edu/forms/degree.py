from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.forms import CustomModelForm

from .. import models


class DegreeForm(CustomModelForm):
    is_academic = forms.ChoiceField(
        choices=models.Degree.AcademicChoices,
        label=_("is academic"),
        initial=models.Degree.AcademicChoices.ACADEMIC,
    )

    class Meta:
        model = models.Degree
        fields = ("name", "order", "is_academic", "description")
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("e.g. Bachelor")),
            "order": widgets.get_number_widget(placeholder=_("e.g. 1")),
            "description": widgets.get_textarea_widget(),
        }
