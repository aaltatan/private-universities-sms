from abc import ABC, abstractmethod

from apps.core.utils import get_apps_links
from apps.core.schemas import AppLink


class IndexMixin(ABC):
    @property
    @abstractmethod
    def page_title(self) -> str:
        pass

    @property
    @abstractmethod
    def app_title(self) -> str:
        pass

    def get_template_names(self) -> list[str]:
        return [f"apps/{self.app_title}/index.html"]

    def get_permissions(self) -> list[str]:
        permissions = [link.perm for link in self.get_apps_links()]
        return permissions

    def get_apps_links(self) -> list[AppLink]:
        return get_apps_links(
            self.request,
            self.app_title,
            unlinked_models=[
                "employee_groups",
                "email",
                "phone",
                "mobile",
                "voucherproxy",
            ],
        )

    def get_context_data(self, **kwargs):
        links = self.get_apps_links()
        return {
            "links": links,
            "page_title": self.page_title.title(),
            **kwargs,
        }

    def get_permission_required(self, request):
        return {
            "any": self.get_permissions(),
        }
