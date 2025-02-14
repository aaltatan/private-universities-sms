from django.utils.translation import gettext as _
from import_export import fields, resources


class BaseResource(resources.ModelResource):
    """
    Fields name, description, slug
    """
    name = fields.Field(
        attribute="name",
        column_name=_("name").title(),
    )
    description = fields.Field(
        attribute="description",
        column_name=_("description").title(),
    )
    slug = fields.Field(
        attribute="slug",
        column_name=_("slug").title(),
    )