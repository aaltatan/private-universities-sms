from apps.core.utils import Deleter

from .models import Currency


class CurrencyDeleter(Deleter[Currency]):
    def check_obj_deleting_possibility(self, obj) -> bool:
        return not obj.is_primary

    def check_queryset_deleting_possibility(self, qs) -> bool:
        return not qs.filter(is_primary=True).exists()
