from django.urls import path
from django.utils.translation import gettext as _

from ..views.ledger import LedgerView


app_name = "ledger"


urlpatterns = [
    path(
        route="<str:slug>/",
        view=LedgerView.as_view(),
        name="index",
        kwargs={"title": _("ledger")},
    ),
]
