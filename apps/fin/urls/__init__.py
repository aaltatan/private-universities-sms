from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("financial")}),
    path("periods/", include("apps.fin.urls.periods")),
    path("years/", include("apps.fin.urls.years")),
    path("taxes/", include("apps.fin.urls.taxes")),
    path("tax-brackets/", include("apps.fin.urls.tax_brackets")),
    path("compensations/", include("apps.fin.urls.compensations")),
    path("voucher-kinds/", include("apps.fin.urls.voucher_kinds")),
]
