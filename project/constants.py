from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext as _
from django.urls import reverse

from apps.core.utils import get_apps_links
from apps.core.schemas import AppLink


def constants(request: HttpRequest) -> dict[str, Any]:
    dashboard_link = AppLink(
        icon="chart-pie",
        text=_("dashboard"),
        path=reverse("core:dashboard"),
    )

    data = {
        "project_name": "Salaries Management System",
        "settings": {
            "messages_timeout": settings.MESSAGES_TIMEOUT,
            "per_page_array": settings.PER_PAGE_ARRAY,
            "per_page": settings.PER_PAGE,
        },
        "sidebar_links": get_apps_links(
            request=request,
            additional_links=[dashboard_link],
            unlinked_apps=["apps.employees"],
        ),
    }
    return data
