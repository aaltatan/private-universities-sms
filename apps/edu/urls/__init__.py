from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView


patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("education")}),
    path("school-kinds/", include("apps.edu.urls.school_kinds")),
    path("schools/", include("apps.edu.urls.schools")),
    path("specializations/", include("apps.edu.urls.specializations")),
    path("degrees/", include("apps.edu.urls.degrees")),
]
