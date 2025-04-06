from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.edu.views import IndexView as EduIndexView
from apps.fin.views import IndexView as FinIndexView
from apps.geo.views import IndexView as GeoIndexView
from apps.hr.views import IndexView as HRIndexView
from apps.org.views import IndexView as OrgIndexView

from .router import router

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "i18n/",
        include("django.conf.urls.i18n"),
    ),
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    # api
    path(
        "api/",
        include(router.urls),
    ),
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # apps
    path(
        "",
        include("apps.core.urls"),
    ),
    path(
        "geo/",
        include(
            [
                path(
                    "",
                    GeoIndexView.as_view(),
                    kwargs={"title": _("geographical")},
                ),
                path(
                    "governorates/",
                    include("apps.geo.urls.governorates"),
                ),
                path(
                    "cities/",
                    include("apps.geo.urls.cities"),
                ),
                path(
                    "nationalities/",
                    include("apps.geo.urls.nationalities"),
                ),
            ]
        ),
    ),
    path(
        "org/",
        include(
            [
                path(
                    "",
                    OrgIndexView.as_view(),
                    kwargs={"title": _("organization")},
                ),
                path(
                    "job-types/",
                    include("apps.org.urls.job_types"),
                ),
                path(
                    "job-subtypes/",
                    include("apps.org.urls.job_subtypes"),
                ),
                path(
                    "groups/",
                    include("apps.org.urls.groups"),
                ),
                path(
                    "cost-centers/",
                    include("apps.org.urls.cost_centers"),
                ),
                path(
                    "positions/",
                    include("apps.org.urls.positions"),
                ),
                path(
                    "statuses/",
                    include("apps.org.urls.statuses"),
                ),
            ]
        ),
    ),
    path(
        "edu/",
        include(
            [
                path(
                    "",
                    EduIndexView.as_view(),
                    kwargs={"title": _("education")},
                ),
                path(
                    "school-kinds/",
                    include("apps.edu.urls.school_kinds"),
                ),
                path(
                    "schools/",
                    include("apps.edu.urls.schools"),
                ),
                path(
                    "specializations/",
                    include("apps.edu.urls.specializations"),
                ),
                path(
                    "degrees/",
                    include("apps.edu.urls.degrees"),
                ),
            ]
        ),
    ),
    path(
        "hr/",
        include(
            [
                path(
                    "",
                    HRIndexView.as_view(),
                    kwargs={"title": _("human resources")},
                ),
                path(
                    "employees/",
                    include("apps.hr.urls.employees"),
                ),
            ]
        ),
    ),
    path(
        "fin/",
        include(
            [
                path(
                    "",
                    FinIndexView.as_view(),
                    kwargs={"title": _("finance")},
                ),
                path(
                    "currencies/",
                    include("apps.fin.urls.currencies"),
                ),
                path(
                    "exchange-rates/",
                    include("apps.fin.urls.exchange_rates"),
                ),
            ]
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
