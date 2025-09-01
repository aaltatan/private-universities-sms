from typing import Literal

from django.utils.translation import gettext_lazy as _

ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "fullname": _("full name"),
    "firstname": _("first name"),
    "lastname": _("last name"),
    "father_name": _("father name"),
    "father_fullname": _("father full name"),
    "mother_name": _("mother name"),
    "birth_place": _("birth place"),
    "birth_date": _("birth date"),
    "national_id": _("national id"),
    "passport_id": _("passport id"),
    "card_id": _("card id"),
    "civil_registry_office": _("civil registry office"),
    "registry_office_name": _("registry office name"),
    "registry_office_id": _("registry office id"),
    "gender": _("gender"),
    "face_color": _("face color"),
    "eyes_color": _("eyes color"),
    "address": _("address"),
    "special_signs": _("special signs"),
    "card_date": _("card date"),
    "martial_status": _("martial status"),
    "military_status": _("military status"),
    "religion": _("religion"),
    "current_address": _("current address"),
    "nationality__name": _("nationality"),
    "city__name": _("city"),
    "hire_date": _("hire date"),
    "separation_date": _("separation date"),
    "cost_center__name": _("cost center"),
    "position__name": _("position"),
    "status__name": _("status"),
    "status__is_payable": _("payable?"),
    "status__is_separated": _("separated?"),
    "job_subtype__name": _("job subtype"),
    "degree__name": _("degree"),
    "school__name": _("school"),
    "specialization__name": _("specialization"),
}

SEARCH_FIELDS: tuple[str] = (
    "firstname",
    "lastname",
    "father_name",
    "national_id",
    "cost_center__name",
)

SELECT_RELATED_FIELDS = Literal[
    # geo
    "city",
    "city__governorate",
    "nationality",
    # org
    "cost_center",
    "position",
    "status",
    "job_subtype",
    "job_subtype__job_type",
    # edu
    "degree",
    "school",
    "school__kind",
    "school__nationality",
    "specialization",
]

PREFETCH_RELATED_LOOKUPS = Literal["emails", "phones", "mobiles", "groups"]
