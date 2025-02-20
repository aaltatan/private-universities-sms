from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.fields import get_autocomplete_field
from apps.geo.models import Nationality

from . import models


class SchoolForm(forms.ModelForm):
    nationality = get_autocomplete_field(
        queryset=Nationality.objects.all(),
        to_field_name="name",
        attributes={"placeholder": _("search nationalities")},
        app_label="geo",
        model_name="Nationality",
        object_name="nationality",
        field_name="search",
    )
    is_governmental = forms.ChoiceField(
        choices=models.School.OwnershipChoices,
        label=_("is governmental"),
        initial=models.School.OwnershipChoices.GOVERNMENTAL,
        help_text=_("is it governmental or private"),
    )
    is_virtual = forms.ChoiceField(
        choices=models.School.VirtualChoices,
        label=_("is virtual"),
        initial=models.School.VirtualChoices.ORDINARY,
        help_text=_("is it virtual or ordinary"),
    )

    class Meta:
        model = models.School
        fields = (
            "name",
            "nationality",
            "is_governmental",
            "is_virtual",
            "website",
            "email",
            "phone",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("school name")),
            "description": widgets.get_textarea_widget(),
            "email": widgets.get_email_widget(),
            "website": widgets.get_url_widget(),
            "phone": widgets.get_text_widget(
                placeholder=_("phone number").title(),
            ),
        }
