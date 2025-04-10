from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from ..views import IndexView

patterns = [
    path("", IndexView.as_view(), kwargs={"title": _("organization")}),
    path("job-types/", include("apps.org.urls.job_types")),
    path("job-subtypes/", include("apps.org.urls.job_subtypes")),
    path("groups/", include("apps.org.urls.groups")),
    path("cost-centers/", include("apps.org.urls.cost_centers")),
    path("positions/", include("apps.org.urls.positions")),
    path("statuses/", include("apps.org.urls.statuses")),
]
