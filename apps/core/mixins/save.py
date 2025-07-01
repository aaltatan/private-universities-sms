from django.contrib.contenttypes.models import ContentType

from ..middlewares import RequestMiddleware
from ..models import Activity


class AddCreateActivityMixin:
    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        request = RequestMiddleware.get_current_request()
        adding: bool = self._state.adding
        super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        if request and self.pk is not None and adding:
            Activity.objects.create(
                user=request.user,
                kind=Activity.KindChoices.CREATE,
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk,
            )
