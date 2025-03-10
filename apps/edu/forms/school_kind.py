from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets

from .. import models


class SchoolKindForm(forms.ModelForm):
    is_governmental = forms.ChoiceField(
        choices=models.SchoolKind.OwnershipChoices,
        label=_("is governmental"),
        initial=models.SchoolKind.OwnershipChoices.GOVERNMENTAL,
        help_text=_("is it governmental or private"),
    )
    is_virtual = forms.ChoiceField(
        choices=models.SchoolKind.VirtualChoices,
        label=_("is virtual"),
        initial=models.SchoolKind.VirtualChoices.ORDINARY,
        help_text=_("is it virtual or ordinary"),
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
            "name": widgets.get_text_widget(placeholder=_("school kind name")),
            "description": widgets.get_textarea_widget(),
        }
