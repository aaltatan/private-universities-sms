from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets

from .. import models


class BaseSchoolForm(forms.ModelForm):
    website = forms.URLField(
        required=False, assume_scheme="https", widget=widgets.get_url_widget()
    )

    class Meta:
        model = models.School
        fields = (
            "name",
            "kind",
            "nationality",
            "website",
            "email",
            "phone",
            "address",
            "description",
        )
        widgets = {
            "name": widgets.get_text_widget(
                placeholder=_("e.g. AlWatniya Private University")
            ),
            "description": widgets.get_textarea_widget(),
            "email": widgets.get_email_widget(),
            "phone": widgets.get_text_widget(
                placeholder=_("e.g. 0947302503"),
            ),
            "address": widgets.get_text_widget(
                placeholder=_("e.g. Warsaw, Poland"),
            ),
        }


class SchoolForm(BaseSchoolForm):
    pass
