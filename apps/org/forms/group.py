from django.utils.translation import gettext_lazy as _

from apps.core.widgets import get_text_widget, get_textarea_widget
from apps.core.forms import CustomModelForm

from .. import models


class GroupForm(CustomModelForm):
    class Meta:
        model = models.Group
        fields = ("name", "kind", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Financial Department")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }
