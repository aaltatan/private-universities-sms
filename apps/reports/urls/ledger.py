from django.urls import path
from django.utils.translation import gettext as _

from ..views.ledger import LedgerView, ExportToMSWordView


app_name = "ledger"


urlpatterns = [
    path(
        route="<str:slug>/",
        view=LedgerView.as_view(),
        name="index",
        kwargs={"title": _("ledger")},
    ),
    path(
        route="msword/<str:slug>/",
        view=ExportToMSWordView.as_view(),
        name="msword",
        kwargs={"title": _("export to MSWord")},
    ),
]
