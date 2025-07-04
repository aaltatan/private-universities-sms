from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin

from apps.core import mixins
from apps.core.utils import Deleter

from .. import filters, models, resources


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "trans.view_journalentry"
    model = models.JournalEntry
    filter_class = filters.JournalEntryFilter
    resource_class = resources.JournalEntryResource
    deleter = Deleter
    order_filter = False

    def get_actions(self):
        return {}
