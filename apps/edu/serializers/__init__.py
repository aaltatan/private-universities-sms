from .degree import DegreeActivitySerializer, DegreeSerializer
from .school import SchoolActivitySerializer, SchoolSerializer, CreateUpdateSchoolSerializer
from .school_kind import SchoolKindActivitySerializer, SchoolKindSerializer
from .specialization import SpecializationActivitySerializer, SpecializationSerializer

__all__ = [
    "DegreeActivitySerializer",
    "DegreeSerializer",
    "SchoolActivitySerializer",
    "CreateUpdateSchoolSerializer",
    "SchoolSerializer",
    "SchoolKindActivitySerializer",
    "SchoolKindSerializer",
    "SpecializationActivitySerializer",
    "SpecializationSerializer",
]