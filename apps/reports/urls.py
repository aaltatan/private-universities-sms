from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views.ledger import LedgerView

app_name = "reports"


urlpatterns = [
    path(
        route="ledger/<str:slug>/",
        view=LedgerView.as_view(),
        name="ledger",
        kwargs={"title": _("ledger")},
    ),
]
