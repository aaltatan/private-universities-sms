from braces.views import MultiplePermissionsRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.core.mixins import IndexMixin


class IndexView(IndexMixin, MultiplePermissionsRequiredMixin, TemplateView):
    page_title = _("transactions")
    app_title = "trans"
