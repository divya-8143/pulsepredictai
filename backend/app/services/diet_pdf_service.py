import io
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class DietPlanPDFService:
    """
    Generates high-resolution clinical-grade Cardioprotective Nutrition & Diet Guide PDF.
    """

    @classmethod
    def generate_diet_pdf(
        cls,
        diet_plan: Dict[str, Any],
        patient_name: str = "Patient",
        assessment_id: Optional[str] = None
    ) -> io.BytesIO:
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
            "DietTitle",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#065F46"),
            fontName="Helvetica-Bold"
        )
        subtitle_style = ParagraphStyle(
            "DietSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#047857"),
            fontName="Helvetica-Bold"
        )
        section_heading = ParagraphStyle(
            "DietHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#065F46"),
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "DietBody",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#1F2937")
        )
        body_bold = ParagraphStyle(
            "DietBodyBold",
            parent=body_style,
            fontName="Helvetica-Bold"
        )
        small_style = ParagraphStyle(
            "DietSmall",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#4B5563")
        )

        story = []

        header_data = [
            [
                Paragraph("<b>PulsePredict AI</b><br/><font size=8 color='#047857'>Cardioprotective Nutrition Engine</font>", subtitle_style),
                Paragraph(f"<b>PATIENT NUTRITION BLUEPRINT</b><br/><font size=8 color='#6B7280'>Date: {datetime.utcnow().strftime('%B %d, %Y')}</font>", ParagraphStyle("RightH", parent=small_style, alignment=2))
            ]
        ]
        t_header = Table(header_data, colWidths=[270, 270])
        t_header.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(t_header)
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#10B981"), spaceAfter=10, spaceBefore=6))

        framework_title = diet_plan.get("primary_dietary_framework", "Cardioprotective Nutrition Protocol")
        weight_goal = diet_plan.get("weight_goal", "Optimal Metabolic Balance")
        calories = diet_plan.get("daily_target_calories", 2000)

        hero_data = [
            [
                Paragraph(f"<b>{framework_title}</b><br/><font size=9 color='#065F46'>{weight_goal}</font>", title_style),
                Paragraph(f"<font size=8 color='#047857'>DAILY TARGET</font><br/><b><font size=18 color='#065F46'>{calories}</font></b><br/><font size=8 color='#047857'>kcal / day</font>", ParagraphStyle("Cal", parent=body_style, alignment=1))
            ]
        ]
        t_hero = Table(hero_data, colWidths=[420, 120])
        t_hero.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
            ("PADDING", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(t_hero)
        story.append(Spacer(1, 10))

        macros = diet_plan.get("macronutrients", {})
        carbs = macros.get("carbohydrates", {"grams": 220, "percentage": 45})
        protein = macros.get("protein", {"grams": 115, "percentage": 23})
        fats = macros.get("healthy_fats", {"grams": 70, "percentage": 32})

        macro_data = [
            [
                Paragraph("<b>Complex Carbohydrates</b>", body_bold),
                Paragraph("<b>Lean Protein</b>", body_bold),
                Paragraph("<b>Healthy Unsaturated Fats</b>", body_bold)
            ],
            [
                Paragraph(f"<font size=12 color='#065F46'><b>{carbs.get('percentage')}%</b></font> ({carbs.get('grams')}g/day)", body_style),
                Paragraph(f"<font size=12 color='#1E40AF'><b>{protein.get('percentage')}%</b></font> ({protein.get('grams')}g/day)", body_style),
                Paragraph(f"<font size=12 color='#B45309'><b>{fats.get('percentage')}%</b></font> ({fats.get('grams')}g/day)", body_style)
            ]
        ]
        t_macros = Table(macro_data, colWidths=[180, 180, 180])
        t_macros.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        story.append(t_macros)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Structured Daily Meal Blueprint", section_heading))
        meals = diet_plan.get("daily_meal_plan", {})
        meal_rows = [
            [Paragraph("<b>Meal Period</b>", body_bold), Paragraph("<b>Menu & Portion Guidelines</b>", body_bold), Paragraph("<b>Clinical Mechanism</b>", body_bold)]
        ]

        for m_key, m_info in meals.items():
            title_txt = f"<b>{m_key.replace('_', ' ').upper()}</b><br/><font size=7 color='#6B7280'>~{m_info.get('calories', '')} kcal</font>"
            items_txt = "<br/>• ".join(["<b>" + m_info.get("title", "") + "</b>"] + m_info.get("items", []))
            rationale_txt = f"<font color='#065F46'>{m_info.get('clinical_rationale', '')}</font>"
            meal_rows.append([
                Paragraph(title_txt, body_style),
                Paragraph("• " + items_txt, small_style),
                Paragraph(rationale_txt, small_style)
            ])

        t_meals = Table(meal_rows, colWidths=[90, 270, 180])
        t_meals.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_meals)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Nutritional Prioritization Matrix", section_heading))
        embrace = diet_plan.get("foods_to_embrace", [])
        restrict = diet_plan.get("foods_to_restrict", [])

        embrace_txt = "<br/>• ".join(["<b>Foods to Prioritize Daily:</b>"] + embrace)
        restrict_txt = "<br/>• ".join(["<b>Foods to Limit / Eliminate:</b>"] + restrict)

        food_matrix_data = [
            [Paragraph(embrace_txt, small_style), Paragraph(restrict_txt, small_style)]
        ]
        t_food_matrix = Table(food_matrix_data, colWidths=[270, 270])
        t_food_matrix.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#ECFDF5")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FFF1F2")),
            ("BOX", (0, 0), (0, 0), 1, colors.HexColor("#A7F3D0")),
            ("BOX", (1, 0), (1, 0), 1, colors.HexColor("#FECDD3")),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_food_matrix)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Micronutrient Limits & Synergistic Habits", section_heading))
        micro_dict = diet_plan.get("micronutrient_targets", {})
        habits = diet_plan.get("lifestyle_habits", [])

        micro_txt = "<br/>• ".join([f"<b>{k.replace('_', ' ').title()}:</b> {v}" for k, v in micro_dict.items()])
        habit_txt = "<br/>• ".join(["<b>Cardiometabolic Habits:</b>"] + habits)

        rules_data = [
            [Paragraph(micro_txt, small_style), Paragraph(habit_txt, small_style)]
        ]
        t_rules = Table(rules_data, colWidths=[270, 270])
        t_rules.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_rules)
        story.append(Spacer(1, 10))

        disclaimer_txt = (
            "<b>Clinical Disclaimer:</b> This dietary recommendation is generated based on computerized clinical guideline matching (ACC/AHA/ADA/DASH). "
            "It is intended for lifestyle optimization and cardiovascular risk mitigation. Patients with advanced renal impairment, heart failure fluid restrictions, "
            "or active pharmacotherapy should review all dietary modifications with their primary physician or registered dietitian."
        )
        story.append(Paragraph(disclaimer_txt, ParagraphStyle("Disc", parent=small_style, textColor=colors.HexColor("#9CA3AF"))))

        doc.build(story)
        buffer.seek(0)
        return buffer
