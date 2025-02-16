from django.urls import path, re_path
from django.utils.translation import gettext as _

from ..views import governorates as views


app_name = "governorates"


urlpatterns = [
    re_path(
        route=r"(reports/(?P<report_name>[a-z\-]+)/)?",
        view=views.ListView.as_view(),
        name="index",
        kwargs={"title": _("governorates")},
    ),
    path(
        route="create/",
        view=views.CreateView.as_view(),
        name="create",
        kwargs={"title": _("create")},
    ),
    path(
        route="update/<str:slug>/",
        view=views.UpdateView.as_view(),
        name="update",
        kwargs={"title": _("update")},
    ),
    path(
        route="delete/<str:slug>/",
        view=views.DeleteView.as_view(),
        name="delete",
        kwargs={"title": _("delete")},
    ),
]
