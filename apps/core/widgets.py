from django.forms.widgets import SelectMultiple
from django.template.loader import render_to_string

class OrderByWidget(SelectMultiple):
    """
    An extended SelectMultiple widget that order functionality and styling.
    """
    template_name = "widgets/order_by.html"

    def render(self, name, value, attrs = ..., renderer = ...):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)