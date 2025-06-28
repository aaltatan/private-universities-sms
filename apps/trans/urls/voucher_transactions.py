from django.urls import path
from django.utils.translation import gettext as _

from ..views import voucher_transactions as views

app_name = "voucher_transactions"


urlpatterns = [
    path(
        route="",
        view=views.ListView.as_view(),
        name="index",
        kwargs={"title": _("vouchers")},
    ),
    path(
        route="details/<str:slug>/",
        view=views.DetailsView.as_view(),
        name="details",
        kwargs={"title": ""},
    ),
]
