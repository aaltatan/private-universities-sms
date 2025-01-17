from django.db.models import QuerySet

from apps.core.utils import Deleter


class CityDeleter(Deleter):
    def is_obj_deletable(self) -> bool:
        return True

    def is_qs_deletable(self, qs: QuerySet) -> bool:
        return True
