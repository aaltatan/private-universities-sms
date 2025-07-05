from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AgeGroupChoices(TextChoices):
    CHILDREN = "children", _("children").title()
    TEENAGERS = "10's", _("teenagers").title()
    TWENTIES = "20's", _("twenties").title()
    THIRTIES = "30's", _("thirties").title()
    FORTIES = "40's", _("forties").title()
    FIFTIES = "50's", _("fifties").title()
    SIXTIES = "60's", _("sixties").title()
    SEVENTIES = "70's", _("seventies").title()
    EIGHTIES = "80's", _("eighties").title()
    NINETIES = "90's", _("nineties").title()
    ABOVE_100 = "above 100", _("above 100").title()


class DateUnitsChoices(TextChoices):
    YEAR = "year", _("year").title()
    MONTH = "month", _("month").title()
    DAY = "day", _("day").title()


class CountsGroupedByChoices(TextChoices):
    GENDER = "gender", _("gender").title()
    FACE_COLOR = "face_color", _("face color").title()
    EYES_COLOR = "eyes_color", _("eyes color").title()
    MARTIAL_STATUS = "martial_status", _("martial status").title()
    MILITARY_STATUS = "military_status", _("military status").title()
    RELIGION = "religion", _("religion").title()
    BIRTH_PLACE = "birth_place", _("birth place").title()
    AGE_GROUP = "age_group", _("age group").title()
    JOB_AGE_GROUP = "job_age_group", _("job age group").title()
    # geo
    GOVERNORATE = "city__governorate__name", _("governorate").title()
    CITY = "city__name", _("city").title()
    NATIONALITY = "nationality__name", _("nationality").title()
    # org
    COST_CENTER = "cost_center__name", _("cost center").title()
    POSITION = "position__name", _("position").title()
    STATUS = "status__name", _("status").title()
    IS_PAYABLE = "status__is_payable", _("payable status").title()
    IS_SEPARATED = "status__is_separated", _("separated status").title()
    JOB_TYPE = "job_subtype__job_type__name", _("job type").title()
    JOB_SUBTYPE = "job_subtype__name", _("job subtype").title()
    GROUPS = "groups__name", _("groups").title()
    # edu
    DEGREE = "degree__name", _("degree").title()
    SCHOOL = "school__name", _("school").title()
    SCHOOL_KIND = "school__kind__name", _("school kind").title()
    SPECIALIZATION = "specialization__name", _("specialization").title()
