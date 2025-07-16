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
                    "text": _("dashboard"),
                    "path": reverse("core:dashboard"),
                },
            },
            "geo": {
                "governorates": {
                    "text": _("governorates"),
                    "path": reverse("geo:governorates:index"),
                },
                "cities": {
                    "text": _("cities"),
                    "path": reverse("geo:cities:index"),
                },
                "nationalities": {
                    "text": _("nationalities"),
                    "path": reverse("geo:nationalities:index"),
                },
            },
            "org": {
                "cost_centers": {
                    "text": _("cost centers"),
                    "path": reverse("org:cost_centers:index"),
                },
                "job_types": {
                    "text": _("job types"),
                    "path": reverse("org:job_types:index"),
                },
                "job_subtypes": {
                    "text": _("job subtypes"),
                    "path": reverse("org:job_subtypes:index"),
                },
                "groups": {
                    "text": _("groups"),
                    "path": reverse("org:groups:index"),
                },
                "positions": {
                    "text": _("positions"),
                    "path": reverse("org:positions:index"),
                },
                "statuses": {
                    "text": _("statuses"),
                    "path": reverse("org:statuses:index"),
                },
            },
            "edu": {
                "school_kinds": {
                    "text": _("school kinds"),
                    "path": reverse("edu:school_kinds:index"),
                },
                "schools": {
                    "text": _("schools"),
                    "path": reverse("edu:schools:index"),
                },
                "degrees": {
                    "text": _("degrees"),
                    "path": reverse("edu:degrees:index"),
                },
                "specializations": {
                    "text": _("specializations"),
                    "path": reverse("edu:specializations:index"),
                },
            },
            "fin": {
                "years": {
                    "text": _("years"),
                    "path": reverse("fin:years:index"),
                },
                "periods": {
                    "text": _("periods"),
                    "path": reverse("fin:periods:index"),
                },
                "taxes": {
                    "text": _("taxes"),
                    "path": reverse("fin:taxes:index"),
                },
                "tax_brackets": {
                    "text": _("tax brackets"),
                    "path": reverse("fin:tax_brackets:index"),
                },
                "compensations": {
                    "text": _("compensations"),
                    "path": reverse("fin:compensations:index"),
                },
                "voucher_kinds": {
                    "text": _("voucher kinds"),
                    "path": reverse("fin:voucher_kinds:index"),
                },
            },
            "hr": {
                "employees": {
                    "text": _("employees"),
                    "path": reverse("hr:employees:index"),
                },
            },
            "trans": {
                "vouchers": {
                    "text": _("vouchers"),
                    "path": reverse("trans:vouchers:index"),
                },
                "voucher_transactions": {
                    "text": _("transactions"),
                    "path": reverse("trans:voucher_transactions:index"),
                },
                "journal_entries": {
                    "text": _("journals entries"),
                    "path": reverse("trans:journal_entries:index"),
                },
            },
            "reports": {
                "trial_balance": {
                    "text": _("trial balance"),
                    "path": reverse("reports:trial_balance:index"),
                },
                "cost_centers": {
                    "text": _("cost centers"),
                    "path": reverse("reports:cost_center:index"),
                },
                "periods": {
                    "text": _("periods"),
                    "path": reverse("reports:periods:index"),
                },
                "compensations": {
                    "text": _("compensations"),
                    "path": reverse("reports:compensations:index"),
                },
            },
        },
    }
    return data
