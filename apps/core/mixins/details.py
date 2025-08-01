from django.db.models import Model


class DetailsMixin:
    slug_field = "slug"
    template_name: str | None = None
    model: Model | None = None

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response["Hx-Trigger"] = "showmodal"
        return response

    def get_codename_plural(self) -> str:
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
        codename_plural = self.get_codename_plural()

        template_name = f"components/{app_label}/{codename_plural}/details.html"

        return [template_name]
