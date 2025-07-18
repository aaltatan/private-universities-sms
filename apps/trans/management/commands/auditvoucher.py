from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.core.models import User

from ...models import Voucher


class Command(BaseCommand):
    help = "Audits specific vouchers"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "serials", nargs="+", type=int, help="list of voucher serial"
        )

    def handle(self, *args, **options):
        serials = options.get("serials", [])

        if not serials:
            raise CommandError("voucher serial is required")

        voucher_serials = [f"VOC{serial:012d}" for serial in serials]
        joined_serials = ", ".join(voucher_serials)

        vouchers = Voucher.objects.filter(voucher_serial__in=voucher_serials)

        if not vouchers.exists():
            raise CommandError(f"vouchers {joined_serials} do not exist")

        try:
            admin = User.objects.get(username="admin")
        except User.DoesNotExist:
            raise CommandError("admin user does not exist")

        vouchers.update(is_audited=True, audited_by=admin)

        self.stdout.write(
            self.style.SUCCESS(
                f"Vouchers {joined_serials} have been audited successfully"
            )
        )
