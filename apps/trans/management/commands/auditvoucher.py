from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.core.models import User

from ...models import Voucher


class Command(BaseCommand):
    help = "Audits specific voucher"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("voucher_serial", type=int, help="voucher serial")

    def handle(self, *args, **options):
        serial = options.get("voucher_serial", None)

        if serial is None:
            raise CommandError("voucher serial is required")

        voucher_serial = f"VOC{serial:012d}"

        try:
            voucher: Voucher = Voucher.objects.get(
                voucher_serial=voucher_serial,
            )
        except Voucher.DoesNotExist:
            raise CommandError(f"voucher {voucher_serial} does not exist")

        try:
            admin = User.objects.get(username="admin")
        except User.DoesNotExist:
            raise CommandError("admin user does not exist")

        voucher.audit(audited_by=admin)

        self.stdout.write(
            self.style.SUCCESS(f"Voucher {voucher_serial} audited successfully")
        )
