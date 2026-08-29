from typing import Dict, Any, List, Optional
import math
from datetime import datetime

class PersonalizedDietaryEngine:
    """
    Precision Cardioprotective & Metabolic Nutrition Engine.
    Synthesizes ACC/AHA, ADA, and DASH dietary guidelines to compute customized daily meal plans,
    macronutrient splits, micronutrient targets, and food substitution guides based on patient biomarkers.
    """

    @classmethod
    def generate_diet_plan(cls, biomarkers: Dict[str, Any], risk_category: str = "MODERATE") -> Dict[str, Any]:
        age = float(biomarkers.get("age", 50))
        gender = str(biomarkers.get("gender", "MALE")).upper()
        bmi = float(biomarkers.get("bmi", 26.5))
        sbp = float(biomarkers.get("systolic_bp", 125))
        dbp = float(biomarkers.get("diastolic_bp", 80))
        glucose = float(biomarkers.get("fasting_glucose", 100))
        hba1c = float(biomarkers.get("hba1c", 5.6))
        total_chol = float(biomarkers.get("total_cholesterol", 200))
        ldl = float(biomarkers.get("ldl_cholesterol", 120))
        tg = float(biomarkers.get("triglycerides", 150))
        activity_hrs = float(biomarkers.get("physical_activity_hours_week", 2.5))

        base_weight_kg = bmi * 1.75 * 1.75
        if gender == "MALE":
            bmr = 10 * base_weight_kg + 6.25 * 175 - 5 * age + 5
        else:
            bmr = 10 * base_weight_kg + 6.25 * 162 - 5 * age - 161

        activity_multiplier = 1.2 if activity_hrs < 1.5 else (1.375 if activity_hrs < 4.0 else 1.55)
        tdee = bmr * activity_multiplier

        if bmi >= 30.0:
            target_calories = int(round(tdee - 500, -1))
            weight_goal = "Gentle Caloric Deficit for Sustainable Weight Loss (-0.5 kg/week)"
        elif bmi >= 25.0:
            target_calories = int(round(tdee - 300, -1))
            weight_goal = "Mild Caloric Deficit & Body Recomposition"
        else:
            target_calories = int(round(tdee, -1))
            weight_goal = "Iso-Caloric Maintenance & Optimal Metabolic Vitality"

        target_calories = max(1400, min(2600, target_calories))

        frameworks = []
        if sbp >= 130 or dbp >= 85:
            frameworks.append("DASH (Dietary Approaches to Stop Hypertension)")
        if hba1c >= 5.7 or glucose >= 100:
            frameworks.append("Low-Glycemic Index Mediterranean Protocol")
        if ldl >= 130 or total_chol >= 200 or tg >= 150:
            frameworks.append("Portfolio / Therapeutic Lifestyle Changes (TLC) Lipid-Lowering Diet")
        if not frameworks:
            frameworks.append("Cardioprotective Longevity Mediterranean Diet")

        primary_framework = frameworks[0]

        if "Low-Glycemic" in primary_framework:
            carbs_pct, protein_pct, fat_pct = 40, 25, 35
            sodium_mg = 1800
            fiber_g = 38
        elif "DASH" in primary_framework:
            carbs_pct, protein_pct, fat_pct = 45, 23, 32
            sodium_mg = 1500
            fiber_g = 35
        elif "Portfolio" in primary_framework:
            carbs_pct, protein_pct, fat_pct = 45, 22, 33
            sodium_mg = 2000
            fiber_g = 42
        else:
            carbs_pct, protein_pct, fat_pct = 48, 22, 30
            sodium_mg = 2000
            fiber_g = 32

        carbs_g = int((target_calories * (carbs_pct / 100.0)) / 4.0)
        protein_g = int((target_calories * (protein_pct / 100.0)) / 4.0)
        fat_g = int((target_calories * (fat_pct / 100.0)) / 9.0)

        meal_plan = {
            "breakfast": {
                "title": "Heart-Smart Antioxidant Oatmeal & Omega-3 Bowl",
                "calories": int(target_calories * 0.25),
                "items": [
                    "1/2 cup Steel-cut rolled oats cooked in water or unsweetened almond milk",
                    "1/2 cup Organic wild blueberries or blackberries (anthocyanin rich)",
                    "1 tbsp Ground golden flaxseeds or chia seeds (omega-3 ALA)",
                    "10 Raw walnut halves (endothelial support)",
                    "1 pinch Ceylon cinnamon (glucose stabilization)"
                ],
                "clinical_rationale": "High viscous beta-glucan soluble fiber binds intestinal bile acids to actively lower LDL cholesterol."
            },
            "morning_snack": {
                "title": "Metabolic Vitality Snack",
                "calories": int(target_calories * 0.10),
                "items": [
                    "1 medium Crisp green apple or pear with skin",
                    "1 tbsp Natural raw unsalted almond butter"
                ],
                "clinical_rationale": "Pectin fiber paired with healthy monounsaturated fats provides steady sustained glycemic release."
            },
            "lunch": {
                "title": "Mediterranean Wild Salmon & Rainbow Quinoa Bowl",
                "calories": int(target_calories * 0.35),
                "items": [
                    "120g Wild-caught Alaskan salmon or organic baked tempeh",
                    "1/2 cup Cooked tri-color quinoa",
                    "2 cups Mixed dark leafy greens (baby spinach, arugula, kale)",
                    "1/2 Hass avocado, sliced",
                    "1 tbsp Extra virgin cold-pressed olive oil & freshly squeezed lemon dressing"
                ],
                "clinical_rationale": "Rich in marine EPA/DHA fatty acids and nitric oxide boosting dietary nitrates for arterial vasodilation."
            },
            "afternoon_snack": {
                "title": "Cardio-Protective Crunch",
                "calories": int(target_calories * 0.10),
                "items": [
                    "3/4 cup Low-fat plain Greek yogurt or coconut kefir",
                    "2 tbsp Raw unsalted pumpkin seeds (zinc & magnesium)"
                ],
                "clinical_rationale": "Magnesium acts as a natural vascular smooth muscle relaxant to aid blood pressure regulation."
            },
            "dinner": {
                "title": "Garlic-Herb Grilled Breast / Lentil Medley & Steamed Greens",
                "calories": int(target_calories * 0.20),
                "items": [
                    "120g Skinless organic chicken breast or 1 cup French green lentils",
                    "1.5 cups Steamed broccoli florets, asparagus spears, and sweet bell peppers",
                    "1 small Roasted Japanese sweet potato with skin",
                    "1 tsp Extra virgin olive oil drizzle with fresh rosemary and garlic"
                ],
                "clinical_rationale": "Lean protein and prebiotic plant diversity support gut microbiome TMAO suppression and liver recovery."
            }
        }

        micronutrients = {
            "sodium_limit": f"< {sodium_mg} mg / day",
            "potassium_target": "4,700 mg / day (supports sodium-potassium ATPase pump)",
            "magnesium_target": "420 mg / day (promotes vascular elasticity)",
            "dietary_fiber": f"> {fiber_g} g / day (minimum 10g viscous soluble fiber)",
            "saturated_fat_limit": "< 5-6% of total caloric intake",
            "plant_sterols": "2.0 g / day (actively reduces LDL absorption by 8-10%)",
            "hydration": "2.5 - 3.0 Liters filtered water daily"
        }

        foods_to_embrace = [
            "Extra Virgin Olive Oil (Polyphenol rich, unheated or low heat)",
            "Fatty fish (Wild Salmon, Sardines, Mackerel - 2x weekly)",
            "Legumes & Pulses (Lentils, Chickpeas, Black Beans, Edamame)",
            "Dark leafy greens (Spinach, Kale, Swiss Chard, Arugula)",
            "Berries (Blueberries, Blackberries, Raspberries, Strawberries)",
            "Raw tree nuts (Walnuts, Almonds, Pistachios, Pecans)",
            "Whole grains (Steel-cut Oats, Quinoa, Farro, Brown Rice)"
        ]

        foods_to_restrict = [
            "Processed meats (Bacon, Sausage, Hot Dogs, Cured Deli Meats)",
            "Sugar-sweetened beverages, commercial fruit juices, and sodas",
            "Trans-fats and ultra-processed baked goods / pastries",
            "Excessive table salt, soy sauce, and high-sodium canned soups",
            "Refined white flour, white bread, and ultra-processed crackers",
            "Deep-fried items and commercial hydrogenated vegetable oils"
        ]

        return {
            "patient_biomarkers_summary": {
                "bmi": bmi,
                "blood_pressure": f"{int(sbp)}/{int(dbp)} mmHg",
                "fasting_glucose": f"{glucose} mg/dL",
                "hba1c": f"{hba1c}%",
                "ldl_cholesterol": f"{ldl} mg/dL"
            },
            "primary_dietary_framework": primary_framework,
            "dietary_frameworks_matched": frameworks,
            "weight_goal": weight_goal,
            "daily_target_calories": target_calories,
            "macronutrients": {
                "carbohydrates": {"grams": carbs_g, "percentage": carbs_pct},
                "protein": {"grams": protein_g, "percentage": protein_pct},
                "healthy_fats": {"grams": fat_g, "percentage": fat_pct}
            },
            "micronutrient_targets": micronutrients,
            "daily_meal_plan": meal_plan,
            "foods_to_embrace": foods_to_embrace,
            "foods_to_restrict": foods_to_restrict,
            "lifestyle_habits": [
                "10-Minute post-prandial brisk walk after lunch and dinner to blunts glucose spikes.",
                "Maintain overnight 12-hour fasting window (e.g. 7:30 PM dinner to 7:30 AM breakfast).",
                "Prioritize 7-8 hours of restorative deep sleep for hormonal cortisol and ghrelin balance."
            ],
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
