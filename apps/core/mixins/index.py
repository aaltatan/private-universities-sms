from abc import ABC, abstractmethod


class IndexMixin(ABC):
    @property
    @abstractmethod
    def page_title(self) -> str:
        pass

    @property
    @abstractmethod
    def app_title(self) -> str:
        pass

    @property
    @abstractmethod
    def data(self) -> tuple[tuple[str, str], ...]:
        pass

    def get_template_names(self) -> list[str]:
        return [f"apps/{self.app_title}/index.html"]

    def get_permissions(self) -> list[str]:
        permissions = [
            f"{self.app_title}.view_{object_name}" for _, object_name, _ in self.data
        ]
        return permissions

    def get_context_data(self, **kwargs):
        urls = [
            (text, href)
            for text, object_name, href in self.data
            if self.request.user.has_perm(f"{self.app_title}.view_{object_name}")
        ]
        return {
            "urls": urls,
            "page_title": self.page_title.title(),
            **kwargs,
        }

    def get_permission_required(self, request):
        return {
            "any": self.get_permissions(),
        }
