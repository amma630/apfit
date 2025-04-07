from datetime import datetime

def generate_workout_ai_recommendation(workouts, usda_food_data):
    today = datetime.now().date()
    recent = [w for w in workouts if (today - w.date).days <= 3]

    total_minutes = sum(w.duration for w in recent)
    cardio_days = sum(1 for w in recent if 'cardio' in w.workout_type.lower())
    strength_days = sum(1 for w in recent if 'strength' in w.workout_type.lower())

    total_calories = sum(f.get('calories', 0) for f in usda_food_data)
    total_protein = sum(f.get('protein', 0) for f in usda_food_data)

    if total_minutes > 150:
        return "🧘 You're smashing it! Consider rest or yoga today."
    if cardio_days >= 2 and strength_days == 0:
        return "💪 Time to hit some weights! Add strength today."
    if strength_days >= 2 and cardio_days == 0:
        return "🏃 Try a cardio workout today to mix things up!"
    if total_protein < 30:
        return "🍗 Boost your protein today: eggs, chicken, tofu!"
    if total_calories < 1000:
        return "⚠️ Eat more to fuel your workouts."
    return "🔥 Great balance! Keep going strong!"
