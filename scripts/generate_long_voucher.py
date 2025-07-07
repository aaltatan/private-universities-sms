import random

from apps.fin.models import Compensation
from apps.hr.models import Employee
from apps.trans.models import Voucher, VoucherTransaction


def generate_long_voucher(voucher: Voucher):
    compensation = Compensation.objects.filter(name__contains="ساعة تدريسية").first()

    for idx in range(200):
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
    voucher = Voucher.objects.filter(title__contains="تموز").first()
    generate_long_voucher(voucher)
