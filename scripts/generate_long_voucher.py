import random

from apps.fin.models import Compensation
from apps.hr.models import Employee
from apps.trans.models import Voucher, VoucherTransaction


def generate_long_voucher(voucher: Voucher, voucher_counts: int = 100):
    compensation = Compensation.objects.filter(name__contains="ساعة تدريسية").first()

    for idx in range(voucher_counts):
        vt = VoucherTransaction(
            voucher=voucher,
            employee=random.choice(list(Employee.objects.all()[:100])),
            compensation=compensation,
            quantity=random.choice(
                [idx for idx in range(1, 128) if idx % 12 == 0],
            ),
            value=random.choice([idx for idx in range(8000, 40000, 1000)]),
        )
        vt.save()


def run():
    inputted = input("Enter the number of vouchers to generate: ")
    try:
        vouchers_count = int(inputted)
    except ValueError:
        vouchers_count = 100

    voucher = Voucher.objects.filter(title__contains="تموز").first()
    generate_long_voucher(voucher, vouchers_count)
