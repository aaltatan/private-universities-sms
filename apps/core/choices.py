from django.db import models
from django.utils.translation import gettext as _


class RoundMethodChoices(models.TextChoices):
    ROUND = "round", _("normal").title()
    FLOOR = "floor", _("down").title()
    CEIL = "ceil", _("up").title()
