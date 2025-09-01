from django.db import models
from django.utils.translation import gettext_lazy as _


class RoundMethodChoices(models.TextChoices):
    ROUND = "round", _("normal")
    FLOOR = "floor", _("down")
    CEIL = "ceil", _("up")


class MonthChoices(models.TextChoices):
    JANUARY = "january", _("january")
    FEBRUARY = "february", _("february")
    MARCH = "march", _("march")
    APRIL = "april", _("april")
    MAY = "may", _("may")
    JUNE = "june", _("june")
    JULY = "july", _("july")
    AUGUST = "august", _("august")
    SEPTEMBER = "september", _("september")
    OCTOBER = "october", _("october")
    NOVEMBER = "november", _("november")
    DECEMBER = "december", _("december")


class QuarterChoices(models.TextChoices):
    Q1 = "q1", _("first quarter")
    Q2 = "q2", _("second quarter")
    Q3 = "q3", _("third quarter")
    Q4 = "q4", _("fourth quarter")
