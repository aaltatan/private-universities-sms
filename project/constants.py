from typing import Any

from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _


def constants(request: HttpRequest) -> dict[str, Any]:
    return {
        "project_name": "Salaries Management System",
        "sidebar_links": [
            {
                "href": reverse("core:index"),
                "text": _("dashboard").title(),
                "icon": "chart-bar",
            },
            {
                "href": reverse("governorates:index"),
                "text": _("governorates").title(),
                "icon": "home-modern",
            },
        ],
    }