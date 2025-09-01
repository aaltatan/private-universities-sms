from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AgeGroupChoices(TextChoices):
    CHILDREN = "children", _("children")
    TEENAGERS = "10's", _("teenagers")
    TWENTIES = "20's", _("twenties")
    THIRTIES = "30's", _("thirties")
    FORTIES = "40's", _("forties")
    FIFTIES = "50's", _("fifties")
    SIXTIES = "60's", _("sixties")
    SEVENTIES = "70's", _("seventies")
    EIGHTIES = "80's", _("eighties")
    NINETIES = "90's", _("nineties")
    ABOVE_100 = "above 100", _("above 100")


class DateUnitsChoices(TextChoices):
    YEAR = "year", _("year")
    MONTH = "month", _("month")
    DAY = "day", _("day")


class CountsGroupedByChoices(TextChoices):
    GENDER = "gender", _("gender")
    FACE_COLOR = "face_color", _("face color")
    EYES_COLOR = "eyes_color", _("eyes color")
    MARTIAL_STATUS = "martial_status", _("martial status")
    MILITARY_STATUS = "military_status", _("military status")
    RELIGION = "religion", _("religion")
    BIRTH_PLACE = "birth_place", _("birth place")
    AGE_GROUP = "age_group", _("age group")
    JOB_AGE_GROUP = "job_age_group", _("job age group")
    # geo
    GOVERNORATE = "city__governorate__name", _("governorate")
    CITY = "city__name", _("city")
    NATIONALITY = "nationality__name", _("nationality")
    # org
    COST_CENTER = "cost_center__name", _("cost center")
    POSITION = "position__name", _("position")
    STATUS = "status__name", _("status")
    IS_PAYABLE = "status__is_payable", _("payable status")
    IS_SEPARATED = "status__is_separated", _("separated status")
    JOB_TYPE = "job_subtype__job_type__name", _("job type")
    JOB_SUBTYPE = "job_subtype__name", _("job subtype")
    GROUPS = "groups__name", _("groups")
    # edu
    DEGREE = "degree__name", _("degree")
    SCHOOL = "school__name", _("school")
    SCHOOL_KIND = "school__kind__name", _("school kind")
    SPECIALIZATION = "specialization__name", _("specialization")
