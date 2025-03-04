from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from treebeard.mp_tree import MP_Node

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from .cost_center import CostCenter
from ..constants import departments as constants


class DepartmentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("cost_center")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Department(AbstractUniqueNameModel, MP_Node):
    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="departments",
    )

    objects: DepartmentManager = DepartmentManager()

    class Meta:
        icon = "rectangle-group"
        codename_plural = "departments"
        verbose_name = _("department").title()
        verbose_name_plural = _("departments").title()
        ordering = ("path", "name")
        permissions = (
            ("export_department", "Can export department"),
            ("view_activity_department", "Can view department activity"),
        )


pre_save.connect(slugify_name, sender=Department)
