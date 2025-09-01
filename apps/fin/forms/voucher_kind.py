from django.utils.translation import gettext_lazy as _

from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseVoucherKindForm(CustomModelForm):
    class Meta:
        model = models.VoucherKind
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. salaries")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }


class VoucherKindForm(BaseVoucherKindForm):
    pass
