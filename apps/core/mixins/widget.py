from abc import ABC, abstractmethod
import django_filters as filters


class WidgetViewMixin(ABC):
    @property
    @abstractmethod
    def filterset_class(self) -> type[filters.FilterSet]:
        pass

    def get_queryset(self):
        qs = super().get_queryset()
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["filter"] = self.filterset_class(self.request.GET)
        return kwargs
