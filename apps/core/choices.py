from django.db import models
from django.utils.translation import gettext as _


class RoundMethodChoices(models.TextChoices):
    ROUND = "round", _("normal").title()
    FLOOR = "floor", _("down").title()
    CEIL = "ceil", _("up").title()


class MonthChoices(models.TextChoices):
    JANUARY = "january", _("january").title()
    FEBRUARY = "february", _("february").title()
    MARCH = "march", _("march").title()
    APRIL = "april", _("april").title()
    MAY = "may", _("may").title()
    JUNE = "june", _("june").title()
    JULY = "july", _("july").title()
    AUGUST = "august", _("august").title()
    SEPTEMBER = "september", _("september").title()
    OCTOBER = "october", _("october").title()
    NOVEMBER = "november", _("november").title()
    DECEMBER = "december", _("december").title()


class QuarterChoices(models.TextChoices):
    Q1 = "q1", _("first quarter").title()
    Q2 = "q2", _("second quarter").title()
    Q3 = "q3", _("third quarter").title()
    Q4 = "q4", _("fourth quarter").title()
