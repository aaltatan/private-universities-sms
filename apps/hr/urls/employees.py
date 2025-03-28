from django.urls import include, path
from django.utils.translation import gettext as _

from ..views import employees as views
from ..views import widgets

app_name = "employees"


urlpatterns = [
    path(
        route="",
        view=views.ListView.as_view(),
        name="index",
        kwargs={"title": _("employees")},
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
        route="widgets/",
        view=include(
            [
                path(
                    route="upcoming-birthdays/",
                    view=widgets.UpcomingBirthdaysView.as_view(),
                    name="upcoming-birthdays",
                ),
                path(
                    route="group-by-counts/",
                    view=widgets.GroupByCountsView.as_view(),
                    name="group-by-counts",
                ),
            ],
        ),
    ),
]
