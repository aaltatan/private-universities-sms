from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.edu.urls import patterns as edu_patterns
from apps.fin.urls import patterns as fin_patterns
from apps.geo.urls import patterns as geo_patterns
from apps.hr.urls import patterns as hr_patterns
from apps.org.urls import patterns as org_patterns
from apps.reports.urls import urlpatterns as reports_patterns
from apps.trans.urls import patterns as trans_patterns

from .router import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # api
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # apps
    path("", include("apps.core.urls")),
    path("geo/", include((geo_patterns, "geo"))),
    path("org/", include((org_patterns, "org"))),
    path("edu/", include((edu_patterns, "edu"))),
    path("fin/", include((fin_patterns, "fin"))),
    path("hr/", include((hr_patterns, "hr"))),
    path("trans/", include((trans_patterns, "trans"))),
    path("reports/", include((reports_patterns, "reports"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
