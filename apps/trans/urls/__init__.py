from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("transactions")}),
    path("vouchers/", include("apps.trans.urls.vouchers")),
    path("vouchers-transactions/", include("apps.trans.urls.voucher_transactions")),
]
