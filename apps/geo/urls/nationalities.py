from django.urls import path
from django.utils.translation import gettext as _

from ..views import nationalities as views


app_name = "nationalities"


urlpatterns = [
    path(
        route="",
        view=views.ListView.as_view(),
        name="index",
        kwargs={"title": _("nationalities")},
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
