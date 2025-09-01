from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..views.cost_centers import CostCenterView


app_name = "cost_center"


urlpatterns = [
    path(
        route="",
        view=CostCenterView.as_view(),
        name="index",
        kwargs={"title": _("cost centers")},
    ),
]
