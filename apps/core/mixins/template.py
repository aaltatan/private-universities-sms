from abc import ABC, abstractmethod
from typing import Any

from django.http import HttpResponse
from docxtpl import DocxTemplate


class ExportToMSWordMixin(ABC):
    @property
    @abstractmethod
    def template(self) -> Any:
        pass

    @abstractmethod
    def get_context_data(self):
        pass

    def get(self, request, *args, **kwargs):
        response = self.render_to_word_response(file=self.template)
        return response

    def get_filename(self):
        return "output"

    def render_to_word_response(self, file, context: dict | None = None):
        if context is None:
            context = self.get_context_data()

        doc = DocxTemplate(file)
        doc.render(context)

        filename = self.get_filename()

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}.docx"
        doc.save(response)

        return response
