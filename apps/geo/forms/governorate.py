from django.utils.translation import gettext_lazy as _

from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class GovernorateForm(CustomModelForm):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Al-Bayda")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }
