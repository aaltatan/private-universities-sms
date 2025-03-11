from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.fields import get_autocomplete_field
from apps.geo.models import Nationality

from .. import models


class BaseSchoolForm(forms.ModelForm):
    website = forms.URLField(required=False, assume_scheme="https")

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
            "name": widgets.get_text_widget(placeholder=_("school name")),
            "description": widgets.get_textarea_widget(),
            "email": widgets.get_email_widget(),
            "website": widgets.get_url_widget(),
            "phone": widgets.get_text_widget(
                placeholder=_("phone number").title(),
            ),
            "address": widgets.get_text_widget(
                placeholder=_("address").title(),
            ),
        }


class SchoolForm(BaseSchoolForm):
    nationality = get_autocomplete_field(
        queryset=Nationality.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search nationalities")},
        app_label="geo",
        model_name="Nationality",
        object_name="nationality",
        field_name="search",
    )
    kind = get_autocomplete_field(
        queryset=models.SchoolKind.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search school kinds")},
        app_label="edu",
        model_name="Schoolkind",
        object_name="schoolkind",
        field_name="search",
    )
