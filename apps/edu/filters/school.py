from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import schools as constants


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


class SchoolFilter(
    FilterComboboxMixin,
    BaseQSearchFilter,
    BaseSchoolFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
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
