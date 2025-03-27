from django.utils.translation import gettext as _
from import_export import fields, resources, widgets

from apps.core.resources import DehydrateBooleanMixin, SerialResourceMixin

from . import models


class EmployeeResource(
    DehydrateBooleanMixin,
    SerialResourceMixin,
    resources.ModelResource,
):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    fullname = fields.Field(
        column_name=_("fullname").title(),
    )
    shortname = fields.Field(
        column_name=_("shortname").title(),
    )
    firstname = fields.Field(
        attribute="firstname",
        column_name=_("first name").title(),
    )
    lastname = fields.Field(
        attribute="lastname",
        column_name=_("last name").title(),
    )
    father_name = fields.Field(
        attribute="father_name",
        column_name=_("father name").title(),
    )
    father_fullname = fields.Field(
        column_name=_("father fullname").title(),
    )
    mother_name = fields.Field(
        attribute="mother_name",
        column_name=_("mother name").title(),
    )
    birth_place = fields.Field(
        attribute="birth_place",
        column_name=_("birth place").title(),
    )
    birth_date = fields.Field(
        attribute="birth_date",
        column_name=_("birth date").title(),
        widget=widgets.DateWidget(coerce_to_string=False),
    )
    age = fields.Field(
        column_name=_("age").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    national_id = fields.Field(
        attribute="national_id",
        column_name=_("national id").title(),
    )
    card_id = fields.Field(
        attribute="card_id",
        column_name=_("card id").title(),
    )
    passport_id = fields.Field(
        attribute="passport_id",
        column_name=_("passport id").title(),
    )
    civil_registry_office = fields.Field(
        attribute="civil_registry_office",
        column_name=_("civil registry office").title(),
    )
    registry_office_name = fields.Field(
        attribute="registry_office_name",
        column_name=_("registry office name").title(),
    )
    registry_office_id = fields.Field(
        attribute="registry_office_id",
        column_name=_("registry office id").title(),
    )
    gender = fields.Field(
        attribute="gender",
        column_name=_("gender").title(),
    )
    face_color = fields.Field(
        attribute="face_color",
        column_name=_("face color").title(),
    )
    eyes_color = fields.Field(
        attribute="eyes_color",
        column_name=_("eyes color").title(),
    )
    address = fields.Field(
        attribute="address",
        column_name=_("address").title(),
    )
    special_signs = fields.Field(
        attribute="special_signs",
        column_name=_("special signs").title(),
    )
    card_date = fields.Field(
        attribute="card_date",
        column_name=_("card date").title(),
        widget=widgets.DateWidget(coerce_to_string=False),
    )
    martial_status = fields.Field(
        attribute="martial_status",
        column_name=_("martial status").title(),
    )
    military_status = fields.Field(
        attribute="military_status",
        column_name=_("military status").title(),
    )
    religion = fields.Field(
        attribute="religion",
        column_name=_("religion").title(),
    )
    current_address = fields.Field(
        attribute="current_address",
        column_name=_("current address").title(),
    )
    nationality = fields.Field(
        attribute="nationality",
        column_name=_("nationality").title(),
    )
    governorate = fields.Field(
        attribute="city__governorate",
        column_name=_("governorate").title(),
    )
    city = fields.Field(
        attribute="city",
        column_name=_("city").title(),
    )
    hire_date = fields.Field(
        attribute="hire_date",
        column_name=_("hire date").title(),
        widget=widgets.DateWidget(coerce_to_string=False),
    )
    job_age = fields.Field(
        column_name=_("job age").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )
    cost_center = fields.Field(
        attribute="cost_center",
        column_name=_("cost center").title(),
    )
    position = fields.Field(
        attribute="position",
        column_name=_("position").title(),
    )
    position_order = fields.Field(
        attribute="position__order",
        column_name=_("position order").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    status = fields.Field(
        attribute="status",
        column_name=_("status").title(),
    )
    is_payable = fields.Field(
        attribute="status__is_payable",
        column_name=_("payable?").title(),
    )
    job_type = fields.Field(
        attribute="job_subtype__job_type",
        column_name=_("job type").title(),
    )
    job_subtype = fields.Field(
        attribute="job_subtype",
        column_name=_("job subtype").title(),
    )
    groups = fields.Field(
        column_name=_("groups").title(),
    )
    groups_with_types = fields.Field(
        column_name=_("groups with types").title(),
    )
    degree = fields.Field(
        attribute="degree",
        column_name=_("degree").title(),
    )
    is_academic = fields.Field(
        attribute="degree__is_academic",
        column_name=_("academic?").title(),
    )
    school = fields.Field(
        attribute="school",
        column_name=_("school").title(),
    )
    school_kind = fields.Field(
        attribute="school__kind",
        column_name=_("school kind").title(),
    )
    school_is_governmental = fields.Field(
        attribute="school__is_governmental",
        column_name=_("governmental school?").title(),
    )
    school_is_virtual = fields.Field(
        attribute="school__is_virtual",
        column_name=_("virtual school?").title(),
    )
    specialization = fields.Field(
        attribute="specialization",
        column_name=_("specialization").title(),
    )
    is_specialist = fields.Field(
        attribute="specialization__is_specialist",
        column_name=_("specialist?").title(),
    )

    def dehydrate_fullname(self, obj: models.Employee):
        return obj.get_fullname()

    def dehydrate_shortname(self, obj: models.Employee):
        return obj.get_shortname()

    def dehydrate_father_fullname(self, obj: models.Employee):
        return obj.get_father_fullname()

    def dehydrate_age(self, obj: models.Employee):
        return obj.age

    def dehydrate_job_age(self, obj: models.Employee):
        return obj.job_age

    def dehydrate_is_payable(self, obj: models.Employee):
        return self._dehydrate_boolean(obj.status.is_payable)

    def dehydrate_groups(self, obj: models.Employee):
        return _(", ").join([obj.name for obj in obj.groups.all()])

    def dehydrate_groups_with_types(self, obj: models.Employee):
        return _(", ").join(
            [f"{obj.name} ({obj.kind})" for obj in obj.groups.all()],
        )

    def dehydrate_is_academic(self, obj: models.Employee):
        return self._dehydrate_boolean(obj.degree.is_academic)

    def dehydrate_school_is_governmental(self, obj: models.Employee):
        return self._dehydrate_boolean(obj.school.kind.is_governmental)

    def dehydrate_school_is_virtual(self, obj: models.Employee):
        return self._dehydrate_boolean(obj.school.kind.is_virtual)

    def dehydrate_is_specialist(self, obj: models.Employee):
        return self._dehydrate_boolean(obj.specialization.is_specialist)

    class Meta:
        model = models.Employee
        fields = (
            "serial",
            "fullname",
            "shortname",
            "firstname",
            "lastname",
            "father_name",
            "father_fullname",
            "mother_name",
            "birth_place",
            "birth_date",
            "age",
            "national_id",
            "card_id",
            "passport_id",
            "civil_registry_office",
            "registry_office_name",
            "registry_office_id",
            "gender",
            "face_color",
            "eyes_color",
            "address",
            "special_signs",
            "card_date",
            "martial_status",
            "military_status",
            "religion",
            "current_address",
            "nationality",
            "governorate",
            "city",
            "hire_date",
            "job_age",
            "notes",
            "cost_center",
            "position",
            "position_order",
            "status",
            "is_payable",
            "job_type",
            "job_subtype",
            "groups",
            "groups_with_types",
            "degree",
            "is_academic",
            "school",
            "school_kind",
            "school_is_governmental",
            "school_is_virtual",
            "specialization",
            "is_specialist",
        )


class BaseInfoResource(SerialResourceMixin, resources.ModelResource):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    employee_name = fields.Field(
        column_name=_("employee name").title(),
    )
    employee_national_id = fields.Field(
        attribute="employee__national_id",
        column_name=_("employee national id").title(),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )

    def dehydrate_employee_name(self, obj: models.Mobile):
        return obj.employee.get_fullname()


class MobileResource(
    BaseInfoResource,
    DehydrateBooleanMixin,
    resources.ModelResource,
):
    number = fields.Field(
        attribute="number",
        column_name=_("number").title(),
    )
    has_whatsapp = fields.Field(
        attribute="has_whatsapp",
        column_name=_("has whatsapp").title(),
    )
    whatsapp_url = fields.Field(
        column_name=_("whatsapp url").title(),
    )

    def dehydrate_has_whatsapp(self, obj: models.Mobile):
        return self._dehydrate_boolean(obj.has_whatsapp)

    def dehydrate_whatsapp_url(self, obj: models.Mobile):
        if obj.has_whatsapp:
            return obj.get_whatsapp_url()
        return ""

    class Meta:
        model = models.Mobile
        fields = (
            "serial",
            "employee_name",
            "employee_national_id",
            "number",
            "kind",
            "has_whatsapp",
            "whatsapp_url",
            "notes",
        )


class PhoneResource(BaseInfoResource, resources.ModelResource):
    number = fields.Field(
        attribute="number",
        column_name=_("number").title(),
    )

    class Meta:
        model = models.Phone
        fields = (
            "serial",
            "employee_name",
            "employee_national_id",
            "number",
            "kind",
            "notes",
        )


class EmailResource(BaseInfoResource, resources.ModelResource):
    email = fields.Field(
        attribute="email",
        column_name=_("email").title(),
    )

    class Meta:
        model = models.Email
        fields = (
            "serial",
            "employee_name",
            "employee_national_id",
            "email",
            "kind",
            "notes",
        )
