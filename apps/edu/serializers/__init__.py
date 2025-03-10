from .degree import DegreeSerializer
from .school import SchoolSerializer, CreateUpdateSchoolSerializer
from .school_kind import SchoolKindSerializer
from .specialization import SpecializationSerializer

__all__ = [
    "DegreeSerializer",
    "CreateUpdateSchoolSerializer",
    "SchoolSerializer",
    "SchoolKindSerializer",
    "SpecializationSerializer",
]
