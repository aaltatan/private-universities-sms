from django.urls import path
from django.utils.translation import gettext as _

from ..views import journal_entries as views

app_name = "journal_entries"


urlpatterns = [
    path(
        route="",
        view=views.ListView.as_view(),
        name="index",
        kwargs={"title": _("journal entries")},
    ),
]
