from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseSchoolFilter(BaseNameDescriptionFilter):
    kind = get_combobox_choices_filter(
        queryset=models.School.objects.all(),
        field_name="kind__name",
        label=_("kind"),
    )
    nationality = get_combobox_choices_filter(
        queryset=models.School.objects.all(),
        field_name="nationality__name",
        label=_("nationality"),
    )
    website = get_text_filter(
        label=_("website"),
        widget_type="url",
        placeholder=_("https://example.com"),
    )
    email = get_text_filter(
        label=_("email"),
        widget_type="email",
        placeholder=_("some-email@example.com"),
    )
    phone = get_text_filter(
        label=_("phone"),
        placeholder=_("phone number"),
    )
    address = get_text_filter(
        label=_("address"),
        placeholder=_("address"),
    )
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.School
        fields = (
            "name",
            "kind",
            "nationality",
            "website",
            "email",
            "phone",
            "address",
            "description",
            "employees_count_from",
            "employees_count_to",
        )


class APISchoolFilter(FilterComboboxMixin, BaseSchoolFilter):
    kind = get_combobox_choices_filter(
        queryset=models.School.objects.all(),
        field_name="kind__name",
        label=_("kind"),
        api_filter=True,
    )
    nationality = get_combobox_choices_filter(
        queryset=models.School.objects.all(),
        field_name="nationality__name",
        label=_("nationality"),
        api_filter=True,
    )


class SchoolFilter(FilterComboboxMixin, BaseSchoolFilter):
    pass
