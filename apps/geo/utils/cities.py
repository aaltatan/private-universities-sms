from django.db.models import QuerySet

from apps.core.utils import BaseDeleter


class Deleter(BaseDeleter):
    def is_obj_deletable(self) -> bool:
        return True

    def is_qs_deletable(self, qs: QuerySet) -> bool:
        return True
