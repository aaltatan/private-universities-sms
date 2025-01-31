from django.urls import path, re_path
from . import views

app_name = "core"

urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "messages/",
        views.messages,
        name="messages",
    ),
    path(
        "activities/<int:object_id>/",
        views.activities,
        name="activities",
    ),
    re_path(
        r"^autocomplete/(?P<pk>\d+)?/?",
        views.AutocompleteView.as_view(),
        name="autocomplete",
    ),
]
