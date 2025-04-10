from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("geographical")}),
    path("governorates/", include("apps.geo.urls.governorates")),
    path("cities/", include("apps.geo.urls.cities")),
    path("nationalities/", include("apps.geo.urls.nationalities")),
]