from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..views.compensations import CompensationsView


app_name = "compensations"


urlpatterns = [
    path(
        route="",
        view=CompensationsView.as_view(),
        name="index",
        kwargs={"title": _("compensations")},
    ),
]
