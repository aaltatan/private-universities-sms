from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("reports")}),
    path("ledger/", include("apps.reports.urls.ledger")),
    path("trial-balance/", include("apps.reports.urls.trial_balance")),
    path("cost-center/", include("apps.reports.urls.cost_center")),
]