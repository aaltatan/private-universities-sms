from django.db import models
from django.db.models.functions import Coalesce
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from .cost_center import CostCenter
from ..constants import departments as constants


class DepartmentManager(TreeManager):
    def get_children(self):
        return self.get_queryset().filter(parent__isnull=False)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("cost_center", "parent")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                parent_department=Coalesce(
                    models.F("parent__name"),
                    models.Value("-"),
                ),
            )
        )


class Department(AbstractUniqueNameModel, MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        blank=True,
        null=True,
    )
    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="departments",
    )

    objects: DepartmentManager = DepartmentManager()

    class MPTTMeta:
        level_attr = "level"
        left_attr = "left"
        right_attr = "right"
        order_insertion_by = ["name"]

    class Meta:
        icon = "rectangle-group"
        title = _("departments")
        ordering = ("name",)
        permissions = (
            ("export_department", "Can export department"),
            ("view_activity_department", "Can view department activity"),
        )


pre_save.connect(slugify_name, sender=Department)
