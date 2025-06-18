from django import forms
from django.utils.translation import gettext as _

from apps.core import fields, widgets
from apps.core.forms import CustomModelForm
from apps.geo.models import Nationality

from .. import models


class BaseSchoolForm(CustomModelForm):
    website = forms.URLField(
        required=False, assume_scheme="https", widget=widgets.get_url_widget()
    )
    kind = fields.get_autocomplete_field(
        models.SchoolKind.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search school kinds")},
        app_label="edu",
        model_name="SchoolKind",
        object_name="school_kind",
        field_name="search",
    )
    nationality = fields.get_autocomplete_field(
        Nationality.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search nationalities")},
        app_label="geo",
        model_name="Nationality",
        object_name="nationality",
        field_name="search",
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
