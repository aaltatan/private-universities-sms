from django.urls import path
from django.utils.translation import gettext as _

from ..views.employees import EmployeesView


app_name = "employees"


urlpatterns = [
    path(
        route="",
        view=EmployeesView.as_view(),
        name="index",
        kwargs={"title": _("employees")},
    ),
]
