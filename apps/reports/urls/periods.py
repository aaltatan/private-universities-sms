from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..views.periods import PeriodsView


app_name = "periods"


urlpatterns = [
    path(
        route="",
        view=PeriodsView.as_view(),
        name="index",
        kwargs={"title": _("periods")},
    ),
]
