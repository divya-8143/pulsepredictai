import enum

class UserRole(str, enum.Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"

class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class SmokingStatus(str, enum.Enum):
    NEVER = "NEVER"
    FORMER = "FORMER"
    CURRENT = "CURRENT"

class AlcoholConsumption(str, enum.Enum):
    NONE = "NONE"
    MODERATE = "MODERATE"
    HEAVY = "HEAVY"

class RiskCategory(str, enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ReviewRecommendation(str, enum.Enum):
    LIFESTYLE_MOD = "LIFESTYLE_MOD"
    CLINICAL_FOLLOWUP = "CLINICAL_FOLLOWUP"
    URGENT_CARE = "URGENT_CARE"
    NO_ACTION = "NO_ACTION"

class DatasetSplit(str, enum.Enum):
    TRAIN = "TRAIN"
    TEST = "TEST"
    VALIDATION = "VALIDATION"
