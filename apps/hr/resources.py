# from django.utils.translation import gettext as _
# from import_export import fields

from apps.core.resources import BaseResource

from . import models


class EmployeeResource(BaseResource):
    class Meta:
        model = models.Employee
        exclude = ("ordering",)
