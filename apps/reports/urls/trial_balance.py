from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..views.trial_balance import TrialBalanceView


app_name = "trial_balance"


urlpatterns = [
    path(
        route="",
        view=TrialBalanceView.as_view(),
        name="index",
        kwargs={"title": _("trial balance")},
    ),
]
