from typing import Any

from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.constants import MESSAGES_TIMEOUT, PER_PAGE_ARRAY, PER_PAGE


def constants(request: HttpRequest) -> dict[str, Any]:
    data = {
        "project_name": "Salaries Management System",
        "settings": {
            "messages_timeout": MESSAGES_TIMEOUT,
            "per_page_array": PER_PAGE_ARRAY,
            "per_page": PER_PAGE,
        },
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
                "perm": "governorates.view_governorate",
            },
            {
                "href": reverse("cities:index"),
                "text": _("cities").title(),
                "icon": "home-modern",
                "perm": "cities.view_city",
            },
        ],
    }
    data["sidebar_links"] = [
        link
        for link in data["sidebar_links"]
        if link.get("perm") is None or request.user.has_perm(link["perm"])
    ]
    return data
