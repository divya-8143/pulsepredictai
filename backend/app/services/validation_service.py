from app.schemas.assessment import HealthDataInput
from app.core.exceptions import ValidationException

class BiomarkerValidationService:
    @staticmethod
    def validate_physiological_coherence(data: HealthDataInput) -> None:
        """
        Enforce clinical physiological consistency rules beyond field-level bounds.
        """
        errors = []

        # 1. Systolic vs Diastolic validation
        if data.systolic_bp <= data.diastolic_bp:
            errors.append(f"Systolic BP ({data.systolic_bp} mmHg) must exceed Diastolic BP ({data.diastolic_bp} mmHg).")

        # 2. Cholesterol partition validation
        if data.total_cholesterol < (data.hdl_cholesterol + data.ldl_cholesterol):
            # Minor physiological leeway allowed, but large discrepancies flagged
            if (data.hdl_cholesterol + data.ldl_cholesterol) - data.total_cholesterol > 40.0:
                errors.append("Sum of HDL and LDL cholesterol significantly exceeds Total Cholesterol.")

        # 3. HbA1c vs Glucose consistency
        if data.hba1c >= 10.0 and data.fasting_glucose < 70.0:
            errors.append("Unrealistically low fasting glucose with severely elevated HbA1c (>= 10.0%).")

        if errors:
            raise ValidationException(
                detail="Biomarker validation failed clinical consistency checks.",
                extra={"clinical_errors": errors}
            )
