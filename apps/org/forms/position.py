from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.forms import CustomModelForm

from .. import models


class PositionForm(CustomModelForm):
    class Meta:
        model = models.Position
        fields = ("name", "order", "description")
        widgets = {
            "name": widgets.get_text_widget(placeholder=_("e.g. Software Developer")),
            "order": widgets.get_number_widget(placeholder=_("e.g. 1")),
            "description": widgets.get_textarea_widget(),
        }
