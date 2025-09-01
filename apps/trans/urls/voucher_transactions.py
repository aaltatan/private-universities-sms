from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..views import voucher_transactions as views

app_name = "voucher_transactions"


urlpatterns = [
    path(
        route="",
        view=views.ListView.as_view(),
        name="index",
        kwargs={"title": _("voucher transactions")},
    ),
]
