from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from apps.fin.views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("finance")}),
    path("currencies/", include("apps.fin.urls.currencies")),
    path("exchange-rates/", include("apps.fin.urls.exchange_rates")),
]
