import math
import re
from datetime import datetime
from decimal import Decimal
from typing import Callable

from django.apps import apps
from django.conf import settings
from django.db.models import Model
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.utils import timezone

from apps.core.schemas import AppLink

from ..constants import ROUND_METHOD


def get_apps_links(
    request: HttpRequest,
    specific_app_label: str | None = None,
    view_name: str = "index",
    additional_links: list[AppLink] = [],
    unlinked_apps: list[str] = [],
    unlinked_models: list[str] = [],
) -> list[AppLink]:
    local_apps = [app for app in settings.LOCAL_APPS if app not in unlinked_apps]
    local_apps = [app.replace("apps.", "") for app in local_apps]

    models = apps.all_models
    models: dict[str, dict[str, Model]] = {
        app: model for app, model in models.items() if app in local_apps
    }

    app_links: list[AppLink] = []

    for app_label, sub_app in models.items():
        for object_name, model in sub_app.items():
            if object_name in unlinked_models:
                continue

            if getattr(model._meta, "codename_plural", None) is None:
                continue

            app_link = AppLink(
                icon=getattr(model._meta, "icon", "star"),
                text=getattr(model._meta, "verbose_name_plural", "some app"),
                path=reverse_lazy(
                    f"{app_label}:{model._meta.codename_plural}:{view_name}",
                ),
                perm=f"{app_label}.view_{object_name}",
            )

            if app_link.perm is None or request.user.has_perm(app_link.perm):
                if specific_app_label is None:
                    app_links.append(app_link)
                else:
                    if app_label == specific_app_label:
                        app_links.append(app_link)

    app_links = [*additional_links, *app_links]

    return app_links


def increase_slug_by_one(slug: str) -> str:
    """
    increases the slug by one.
    """
    if not slug:
        return slug

    slug = slug.lower()
    pattern = re.compile(r"([^0-9]*)(\d+)$")
    match_obj = pattern.match(slug)

    if match_obj:
        number = int(match_obj.groups()[-1]) + 1
        string = match_obj.groups()[0]
        increased_slug = f"{string}{number}"
    else:
        increased_slug = f"{slug}1"

    return increased_slug


def get_differences(from_: dict, to: dict) -> dict:
    """
    Returns the differences between two dictionaries.
    """
    differences: set = set(from_.items()) ^ set(to.items())

    before: dict = {}
    after: dict = {}

    for key, value in differences:
        diff = key, value
        if diff in from_.items():
            before[key] = value
        else:
            after[key] = value

    if differences:
        return {"before": before, "after": after}
    else:
        return {}


def calculate_age_in_years(
    date: datetime,
    other_date: datetime | None = None,
) -> int:
    """
    calculates the age in years.
    """
    if other_date is None:
        other_date = timezone.now().date()

    difference = other_date.year - date.year

    if (other_date.month, other_date.day) < (date.month, date.day):
        difference -= 1

    return difference


def round_to_nearest(
    number: Decimal | int | float, method: ROUND_METHOD = "ceil", to_nearest: int = 100
) -> Decimal:
    """
    rounds a number to the nearest value.
    """
    round_methods: dict[ROUND_METHOD, Callable] = {
        "round": round,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    return Decimal(round_methods[method](number / to_nearest)) * to_nearest
