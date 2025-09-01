from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core import widgets
from apps.core.forms import CustomModelForm

from .. import models


class SchoolKindForm(CustomModelForm):
    is_governmental = forms.ChoiceField(
        choices=models.SchoolKind.OwnershipChoices,
        label=_("is governmental"),
        initial=models.SchoolKind.OwnershipChoices.GOVERNMENTAL,
    )
    is_virtual = forms.ChoiceField(
        choices=models.SchoolKind.VirtualChoices,
        label=_("is virtual"),
        initial=models.SchoolKind.VirtualChoices.ORDINARY,
    )

    class Meta:
        model = models.SchoolKind
        fields = (
            "name",
            "is_governmental",
            "is_virtual",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("e.g. High School")),
            "description": widgets.get_textarea_widget(placeholder=_("some description")),
        }
