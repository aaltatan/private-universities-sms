from django.forms.widgets import SelectMultiple
from django.template.loader import render_to_string


class ComboboxWidget(SelectMultiple):
    """
    An extended SelectMultiple widget that renders a combobox.
    """
    template_name = "widgets/combobox.html"
    checked_attribute = {"checked": True}

    def render(self, name, value, attrs=..., renderer=...):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)


class OrderByWidget(SelectMultiple):
    """
    An extended SelectMultiple widget that order functionality and styling.
    """

    template_name = "widgets/order_by.html"

    def render(self, name, value, attrs=..., renderer=...):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)
