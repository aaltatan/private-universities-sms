from django import forms

from .fields import CustomModelChoiceField


class CustomModelForm(forms.ModelForm):
    """
    A custom ModelForm.

    This class is used to add autocomplete fields to the form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        autocomplete_fields = [
            {field_name: field}
            for field_name, field in self.fields.items()
            if type(field) == CustomModelChoiceField
        ]

        for field in autocomplete_fields:
            field_name, field = list(field.items())[0]
            related_instance = getattr(self.instance, field_name, None)

            if self.instance and related_instance:
                self.initial[field_name] = getattr(
                    related_instance, field.to_field_name
                )
