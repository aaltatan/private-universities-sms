from django.db import models
from django.utils.translation import gettext as _
from solo.models import SingletonModel


class HRSetting(SingletonModel):
    min_employee_age = models.PositiveIntegerField(
        default=18,
        verbose_name=_("min employee age"),
        help_text=_("allowed min employee age"),
    )
    nth_job_anniversary = models.PositiveIntegerField(
        default=2,
        verbose_name=_("nth job anniversary"),
        help_text=_("years count to calculate job anniversary"),
    )
    years_count_to_group_job_age = models.PositiveIntegerField(
        default=2,
        verbose_name=_("years count to group job age"),
        help_text=_("years count to group job age"),
    )

    def __str__(self):
        return "Human Resources Settings"

    class Meta:
        verbose_name = _("hr settings").title()
        ordering = ("id",)
