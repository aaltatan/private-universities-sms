from braces.views import MultiplePermissionsRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from apps.core.mixins import IndexMixin


class IndexView(IndexMixin, MultiplePermissionsRequiredMixin, TemplateView):
    page_title = _("reports")
    app_title = "reports"
