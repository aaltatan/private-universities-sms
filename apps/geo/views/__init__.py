from braces.views import MultiplePermissionsRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from apps.core.mixins import IndexMixin


class IndexView(IndexMixin, MultiplePermissionsRequiredMixin, TemplateView):
    page_title = _("geographical")
    app_title = "geo"
    data = (
        (
            _("governorates"),
            "governorate",
            reverse_lazy("governorates:index"),
        ),
        (
            _("cities"),
            "city",
            reverse_lazy("cities:index"),
        ),
        (
            _("nationalities"),
            "nationality",
            reverse_lazy("nationalities:index"),
        ),
    )
