from django.db.models import Model


class DetailsMixin:
    slug_field = "slug"
    template_name: str | None = None
    model: Model | None = None

    def get_verbose_name_plural(self) -> str:
        return self.model._meta.codename_plural

    def get_app_label(self) -> str:
        return self.model._meta.app_label
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["model"] = self.model
        return context

    def get_template_names(self) -> list[str]:
        if getattr(self, "template_name", None) is not None:
            return self.template_name

        app_label = self.get_app_label()
        verbose_name_plural = self.get_verbose_name_plural()

        template_name = f"components/{app_label}/{verbose_name_plural}/details.html"

        return [template_name]
