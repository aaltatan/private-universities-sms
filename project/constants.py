from typing import Any

from django.http import HttpRequest
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext as _


def constants(request: HttpRequest) -> dict[str, Any]:
    data = {
        "project_name": "Salaries Management System",
        "settings": {
            "messages_timeout": settings.MESSAGES_TIMEOUT,
            "per_page_array": settings.PER_PAGE_ARRAY,
            "per_page": settings.PER_PAGE,
        },
        "sidebar_links": [
            {
                "href": reverse("core:dashboard"),
                "text": _("dashboard").title(),
                "icon": "chart-bar",
            },
            {
                "href": reverse("governorates:index"),
                "text": _("governorates").title(),
                "icon": "home-modern",
                "perm": "geo.view_governorate",
            },
            {
                "href": reverse("cities:index"),
                "text": _("cities").title(),
                "icon": "home-modern",
                "perm": "geo.view_city",
            },
            {
                "href": reverse("nationalities:index"),
                "text": _("nationalities").title(),
                "icon": "globe-europe-africa",
                "perm": "geo.view_nationality",
            },
            {
                "href": reverse("job_types:index"),
                "text": _("job types").title(),
                "icon": "briefcase",
                "perm": "org.view_jobtype",
            },
            {
                "href": reverse("job_subtypes:index"),
                "text": _("job subtypes").title(),
                "icon": "briefcase",
                "perm": "org.view_jobsubtype",
            },
            {
                "href": reverse("groups:index"),
                "text": _("groups").title(),
                "icon": "user-group",
                "perm": "org.view_group",
            },
            {
                "href": reverse("cost_centers:index"),
                "text": _("cost centers").title(),
                "icon": "building-office-2",
                "perm": "org.view_costcenter",
            },
            {
                "href": reverse("positions:index"),
                "text": _("positions").title(),
                "icon": "chevron-double-up",
                "perm": "org.view_position",
            },
            {
                "href": reverse("statuses:index"),
                "text": _("statuses").title(),
                "icon": "check-circle",
                "perm": "org.view_status",
            },
        ],
    }
    data["sidebar_links"] = [
        link
        for link in data["sidebar_links"]
        if link.get("perm") is None or request.user.has_perm(link["perm"])
    ]
    return data
