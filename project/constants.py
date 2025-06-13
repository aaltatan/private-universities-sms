from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext as _
from django.urls import reverse


def constants(request: HttpRequest) -> dict[str, Any]:
    data = {
        "project_name": "Salaries Management",
        "settings": {
            "messages_timeout": settings.MESSAGES_TIMEOUT,
            "per_page_array": settings.PER_PAGE_ARRAY,
            "per_page": settings.PER_PAGE,
        },
        "sidebar_links": {
            "core": {
                "dashboard": {
                    "text": _("dashboard").title(),
                    "path": reverse("core:dashboard"),
                },
            },
            "geo": {
                "governorates": {
                    "text": _("governorates").title(),
                    "path": reverse("geo:governorates:index"),
                },
                "cities": {
                    "text": _("cities").title(),
                    "path": reverse("geo:cities:index"),
                },
                "nationalities": {
                    "text": _("nationalities").title(),
                    "path": reverse("geo:nationalities:index"),
                },
            },
            "org": {
                "cost_centers": {
                    "text": _("cost centers").title(),
                    "path": reverse("org:cost_centers:index"),
                },
                "job_types": {
                    "text": _("job types").title(),
                    "path": reverse("org:job_types:index"),
                },
                "job_subtypes": {
                    "text": _("job subtypes").title(),
                    "path": reverse("org:job_subtypes:index"),
                },
                "groups": {
                    "text": _("groups").title(),
                    "path": reverse("org:groups:index"),
                },
                "positions": {
                    "text": _("positions").title(),
                    "path": reverse("org:positions:index"),
                },
                "statuses": {
                    "text": _("statuses").title(),
                    "path": reverse("org:statuses:index"),
                },
            },
            "edu": {
                "school_kinds": {
                    "text": _("school kinds").title(),
                    "path": reverse("edu:school_kinds:index"),
                },
                "schools": {
                    "text": _("schools").title(),
                    "path": reverse("edu:schools:index"),
                },
                "degrees": {
                    "text": _("degrees").title(),
                    "path": reverse("edu:degrees:index"),
                },
                "specializations": {
                    "text": _("specializations").title(),
                    "path": reverse("edu:specializations:index"),
                },
            },
            "fin": {
                "years": {
                    "text": _("years").title(),
                    "path": reverse("fin:years:index"),
                },
                "periods": {
                    "text": _("periods").title(),
                    "path": reverse("fin:periods:index"),
                },
                "taxes": {
                    "text": _("taxes").title(),
                    "path": reverse("fin:taxes:index"),
                },
                "tax_brackets": {
                    "text": _("tax brackets").title(),
                    "path": reverse("fin:tax_brackets:index"),
                },
                "compensations": {
                    "text": _("compensations").title(),
                    "path": reverse("fin:compensations:index"),
                },
                "voucher_kinds": {
                    "text": _("voucher kinds").title(),
                    "path": reverse("fin:voucher_kinds:index"),
                },
            },
            "hr": {
                "employees": {
                    "text": _("employees").title(),
                    "path": reverse("hr:employees:index"),
                },
            },
            "trans": {
                "vouchers": {
                    "text": _("vouchers").title(),
                    "path": reverse("trans:vouchers:index"),
                },
            },
        },
    }
    return data
