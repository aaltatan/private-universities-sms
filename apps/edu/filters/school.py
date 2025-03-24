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
    website = get_text_filter(
        label=_("website").title(),
        widget_type="url",
        placeholder=_("https://example.com"),
    )
    email = get_text_filter(
        label=_("email").title(),
        widget_type="email",
        placeholder=_("some-email@example.com"),
    )
    phone = get_text_filter(
        label=_("phone").title(),
        placeholder=_("phone number").title(),
    )
    address = get_text_filter(
        label=_("address").title(),
        placeholder=_("address").title(),
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
        model=models.School,
        field_name="kind__name",
        label=_("kind"),
        api_filter=True,
    )
    nationality = get_combobox_choices_filter(
        model=models.School,
        field_name="nationality__name",
        label=_("nationality"),
        api_filter=True,
    )


class SchoolFilter(FilterComboboxMixin, BaseSchoolFilter):
    kind = get_combobox_choices_filter(
        model=models.School,
        field_name="kind__name",
        label=_("kind"),
    )
    nationality = get_combobox_choices_filter(
        model=models.School,
        field_name="nationality__name",
        label=_("nationality"),
    )
