from .email import EmailSerializer
from .employee import EmployeeCreateUpdateSerializer, EmployeeSerializer
from .mobile import MobileSerializer
from .phone import PhoneSerializer

__all__ = [
    "EmailSerializer",
    "EmployeeSerializer",
    "EmployeeCreateUpdateSerializer",
    "MobileSerializer",
    "PhoneSerializer",
]
