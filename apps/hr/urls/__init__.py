from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("human resources")}),
    path("employees/", include("apps.hr.urls.employees")),
]
