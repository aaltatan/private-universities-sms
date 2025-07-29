from pathlib import Path

from django.apps import AppConfig
from django.core.files import File


def _create_template_item(apps: AppConfig, name, template):
    TemplateItem = apps.get_model("core", "TemplateItem")

    with open(template, "rb") as file:
        template_item = TemplateItem()
        template_item.name = f"{name} template"
        template_item.file.save(f"{name}.docx", File(file))
        template_item.save()

        return template_item


def create_default_template(apps: AppConfig, schema_editor):
    employee = Path("assets/word_templates/employee.docx").resolve()
    base_voucher = Path("assets/word_templates/voucher.docx").resolve()
    base_ledger = Path("assets/word_templates/ledger.docx").resolve()

    Template = apps.get_model("core", "Template")

    employee_template_item = _create_template_item(apps, "employee", employee)
    voucher_template_item = _create_template_item(apps, "voucher", base_voucher)
    ledger_template_item = _create_template_item(apps, "ledger", base_ledger)

    Template.objects.create(
        voucher=voucher_template_item,
        employee=employee_template_item,
        ledger=ledger_template_item,
    )
