from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
        "home/",
        include("apps.core.urls"),
    ),
    # geo
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
    # org
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
]

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
