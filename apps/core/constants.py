from typing import Literal


PERMISSION = Literal[
    "view",
    "add",
    "change",
    "delete",
    "export",
    "view_activity",
    "audit",
    "unaudit",
    "migrate",
    "unmigrate",
]

DATE_UNITS = Literal["year", "month", "day"]

ROUND_METHOD = Literal["ceil", "floor", "round"]
