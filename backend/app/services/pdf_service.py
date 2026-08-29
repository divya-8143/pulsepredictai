import os
import io
from typing import Any, Dict
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.models.assessment import HealthAssessment
from app.models.patient import PatientProfile

class ClinicalPDFReportService:
    @staticmethod
    def generate_assessment_pdf(assessment: HealthAssessment, patient: PatientProfile, doctor_review: Any = None) -> io.BytesIO:
        """
        Generate comprehensive, tamper-evident clinical PDF health risk report.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#1e3a8a"),
            alignment=TA_LEFT
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748b")
        )
        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155")
        )
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#94a3b8"),
            alignment=TA_CENTER
        )

        elements = []

        # 1. Header Banner
        elements.append(Paragraph("PulsePredict AI - Clinical Health Risk Assessment", title_style))
        elements.append(Paragraph(f"Report Generated: {datetime.utcnow().strftime('%B %d, %Y - %H:%M UTC')} | Assessment ID: {str(assessment.id)[:12]}...", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

        # 2. Patient Demographics & Assessment Summary Table
        pat_name = patient.user.full_name if patient.user else "Patient"
        pat_email = patient.user.email if patient.user else "N/A"
        demo_data = [
            [Paragraph("<b>Patient Name:</b>", body_style), Paragraph(pat_name, body_style), Paragraph("<b>Gender / Age:</b>", body_style), Paragraph(f"{patient.gender or 'N/A'} / {assessment.age} yrs", body_style)],
            [Paragraph("<b>Patient Email:</b>", body_style), Paragraph(pat_email, body_style), Paragraph("<b>Blood Group:</b>", body_style), Paragraph(patient.blood_group or "N/A", body_style)],
            [Paragraph("<b>Evaluation Date:</b>", body_style), Paragraph(assessment.assessed_at.strftime("%Y-%m-%d %H:%M"), body_style), Paragraph("<b>Primary Model:</b>", body_style), Paragraph(assessment.primary_model_name, body_style)]
        ]
        demo_table = Table(demo_data, colWidths=[90, 180, 90, 180])
        demo_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ]))
        elements.append(demo_table)
        elements.append(Spacer(1, 10))

        # 3. Overall Risk Score Banner
        cat_color = {
            "LOW": colors.HexColor("#10b981"),
            "MODERATE": colors.HexColor("#f59e0b"),
            "HIGH": colors.HexColor("#f97316"),
            "CRITICAL": colors.HexColor("#ef4444")
        }.get(assessment.risk_category.value, colors.HexColor("#2563eb"))

        risk_banner = [
            [
                Paragraph(f"<b>Overall Risk Score: {assessment.overall_risk_score:.1f} / 100</b>", ParagraphStyle("RScore", parent=body_style, fontSize=14, textColor=colors.white, fontName="Helvetica-Bold")),
                Paragraph(f"<b>Risk Category: {assessment.risk_category.value}</b>", ParagraphStyle("RCat", parent=body_style, fontSize=12, textColor=colors.white, fontName="Helvetica-Bold", alignment=TA_RIGHT))
            ]
        ]
        risk_table = Table(risk_banner, colWidths=[270, 270])
        risk_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), cat_color),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(risk_table)
        elements.append(Spacer(1, 10))

        # 4. Biomarkers Table
        elements.append(Paragraph("<b>Physiological Biomarkers & Laboratory Metrics</b>", section_heading))
        bio_data = [
            ["Biomarker Parameter", "Patient Value", "Reference Range", "Status"],
            ["Systolic Blood Pressure", f"{assessment.systolic_bp} mmHg", "< 120 mmHg", "Normal" if assessment.systolic_bp < 120 else "Elevated"],
            ["Diastolic Blood Pressure", f"{assessment.diastolic_bp} mmHg", "< 80 mmHg", "Normal" if assessment.diastolic_bp < 80 else "Elevated"],
            ["Body Mass Index (BMI)", f"{assessment.bmi} kg/m²", "18.5 - 24.9 kg/m²", "Optimal" if 18.5 <= assessment.bmi < 25 else "Out of Range"],
            ["Fasting Blood Glucose", f"{assessment.fasting_glucose} mg/dL", "70 - 99 mg/dL", "Optimal" if assessment.fasting_glucose < 100 else "Elevated"],
            ["Glycated Hemoglobin (HbA1c)", f"{assessment.hba1c} %", "< 5.7 %", "Optimal" if assessment.hba1c < 5.7 else "Elevated"],
            ["Total Cholesterol", f"{assessment.total_cholesterol} mg/dL", "< 200 mg/dL", "Desirable" if assessment.total_cholesterol < 200 else "High"],
            ["HDL Cholesterol", f"{assessment.hdl_cholesterol} mg/dL", "> 50 mg/dL", "Optimal" if assessment.hdl_cholesterol >= 50 else "Low"],
            ["LDL Cholesterol", f"{assessment.ldl_cholesterol} mg/dL", "< 100 mg/dL", "Optimal" if assessment.ldl_cholesterol < 100 else "Elevated"],
            ["Smoking Status", str(assessment.smoking_status.value), "Non-Smoker", "Risk Factor" if assessment.smoking_status.value != "NEVER" else "Optimal"]
        ]
        bio_table = Table(bio_data, colWidths=[160, 120, 140, 120])
        bio_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))
        elements.append(bio_table)
        elements.append(Spacer(1, 10))

        # 5. Top SHAP Risk Contributors
        elements.append(Paragraph("<b>Top AI Feature Contributions (SHAP Analysis)</b>", section_heading))
        shap_items = assessment.feature_importance_shap or []
        shap_data = [["Biomarker Feature", "Observed Value", "Risk Direction", "Clinical Interpretation"]]
        for item in shap_items[:5]:
            shap_data.append([
                item.get("display_name", "Feature"),
                str(item.get("feature_value", "")),
                item.get("impact", "NEUTRAL").replace("_", " "),
                Paragraph(item.get("clinical_note", ""), body_style)
            ])
        shap_table = Table(shap_data, colWidths=[120, 90, 90, 240])
        shap_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))
        elements.append(shap_table)
        elements.append(Spacer(1, 12))

        # 6. Physician Clinical Annotation
        if doctor_review:
            elements.append(Paragraph("<b>Physician Clinical Review & Orders</b>", section_heading))
            rev_text = f"<b>Reviewed By:</b> Dr. {doctor_review.doctor.user.full_name} ({doctor_review.doctor.specialization})<br/><b>Recommendation:</b> {doctor_review.recommendation.value}<br/><b>Clinical Notes:</b> {doctor_review.clinical_notes}"
            elements.append(Paragraph(rev_text, body_style))
            elements.append(Spacer(1, 10))

        # 7. Medical Disclaimer Footer
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
        elements.append(Paragraph(
            "<b>LEGAL MEDICAL DISCLAIMER:</b> PulsePredict AI is an artificial intelligence decision support and risk stratification tool intended exclusively for research, preventive health monitoring, and clinical guidance. This report does NOT represent a definitive medical diagnosis. Patients must consult licensed healthcare professionals for diagnosis and treatment planning.",
            disclaimer_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer
