from django.urls import path
from django.utils.translation import gettext as _

from ..views import vouchers as views

app_name = "vouchers"


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
    path(
        route="audit/<str:slug>/",
        view=views.AuditView.as_view(),
        name="audit",
        kwargs={"title": _("audit")},
    ),
    path(
        route="migrate/<str:slug>/",
        view=views.MigrateView.as_view(),
        name="migrate",
        kwargs={"title": _("migrate")},
    ),
    path(
        route="unmigrate/<str:slug>/",
        view=views.UnMigrateView.as_view(),
        name="unmigrate",
        kwargs={"title": _("unmigrate")},
    ),
]
