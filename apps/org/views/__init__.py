from braces.views import MultiplePermissionsRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from apps.core.mixins import IndexMixin


class IndexView(IndexMixin, MultiplePermissionsRequiredMixin, TemplateView):
    page_title = _("organization")
    app_title = "org"
    data = (
        (
            _("job types"),
            "jobtype",
            reverse_lazy("job_subtypes:index"),
        ),
        (
            _("job subtypes"),
            "jobsubtype",
            reverse_lazy("job_types:index"),
        ),
        (
            _("groups"),
            "group",
            reverse_lazy("groups:index"),
        ),
        (
            _("cost centers"),
            "costcenter",
            reverse_lazy("cost_centers:index"),
        ),
        (
            _("positions"),
            "position",
            reverse_lazy("positions:index"),
        ),
        (
            _("statuses"),
            "status",
            reverse_lazy("statuses:index"),
        ),
    )
