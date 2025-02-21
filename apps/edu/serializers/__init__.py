from .school import SchoolActivitySerializer, SchoolSerializer, CreateUpdateSchoolSerializer
from .school_kind import SchoolKindActivitySerializer, SchoolKindSerializer
from .specialization import SpecializationActivitySerializer, SpecializationSerializer

__all__ = [
    "SchoolActivitySerializer",
    "CreateUpdateSchoolSerializer",
    "SchoolSerializer",
    "SchoolKindActivitySerializer",
    "SchoolKindSerializer",
    "SpecializationActivitySerializer",
    "SpecializationSerializer",
]