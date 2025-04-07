import json
import requests
from datetime import date, timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import MealLog
from .forms import MealLogForm

# Constants
CALORIE_MIN = 1200
CALORIE_MAX = 2200

def get_usda_nutrition(food_name):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    detail_url_base = "https://api.nal.usda.gov/fdc/v1/food/"

    try:
        # Search for food
        search_params = {
            "query": food_name,
            "pageSize": 1,
            "api_key": settings.USDA_API_KEY
        }
        response = requests.get(search_url, params=search_params)
        response.raise_for_status()

        foods = response.json().get("foods", [])
        if not foods:
            return None

        # Get nutrition details
        fdc_id = foods[0]["fdcId"]
        detail_response = requests.get(
            f"{detail_url_base}{fdc_id}",
            params={"api_key": settings.USDA_API_KEY}
        )
        detail_response.raise_for_status()
        data = detail_response.json()

        nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        for nutrient in data.get("foodNutrients", []):
            name = nutrient.get("nutrient", {}).get("name", "").lower()
            value = nutrient.get("amount", 0)

            if 'energy' in name and 'kcal' in nutrient.get("nutrient", {}).get("unitName", "").lower():
                nutrition['calories'] = value
            elif 'protein' in name:
                nutrition['protein'] = value
            elif 'carbohydrate' in name:
                nutrition['carbs'] = value
            elif 'total lipid' in name or 'fat' in name:
                nutrition['fat'] = value

        return nutrition

    except requests.exceptions.RequestException as e:
        print(f"❌ USDA API Request Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error fetching nutrition: {e}")
    return None

@login_required
def meal_log_view(request):
    today = date.today()

    # Handle form submission
    if request.method == 'POST':
        form = MealLogForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            nutrition = get_usda_nutrition(meal.food_name)
            if nutrition:
                meal.total_calories = nutrition['calories']
                meal.protein = nutrition['protein']
                meal.carbs = nutrition['carbs']
                meal.fat = nutrition['fat']
            meal.save()
            return redirect('meal_log')
    else:
        form = MealLogForm()

    # Today's logs
    today_logs = MealLog.objects.filter(user=request.user, date=today)
    total_calories = sum((log.total_calories or 0) for log in today_logs)

    # Nutrition Recommendation
    if total_calories < CALORIE_MIN:
        recommendation = "Eat a bit more — maybe something rich in protein 🍗"
    elif total_calories > CALORIE_MAX:
        recommendation = "You've eaten a lot — try something light 🥗"
    else:
        recommendation = "You're doing great! 🎉"

    # Weekly Data
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_data, weekly_labels, weekly_calories = [], [], []

    for day in week_dates:
        logs = MealLog.objects.filter(user=request.user, date=day)
        calories = sum((log.total_calories or 0) for log in logs)
        protein = sum((log.protein or 0) for log in logs)
        carbs = sum((log.carbs or 0) for log in logs)
        fat = sum((log.fat or 0) for log in logs)

        weekly_data.append({
            'date': day.strftime('%a'),
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat
        })

        weekly_labels.append(day.strftime('%a'))
        weekly_calories.append(calories)

    # Pie chart macros
    today_macros = {
        'protein': sum((log.protein or 0) for log in today_logs),
        'carbs': sum((log.carbs or 0) for log in today_logs),
        'fat': sum((log.fat or 0) for log in today_logs),
    }
        # Calculate percentages for today_macros
    total_macros = sum(today_macros.values()) or 1  # avoid division by zero
    macro_percentages = {
        'protein': round((today_macros['protein'] / total_macros) * 100),
        'carbs': round((today_macros['carbs'] / total_macros) * 100),
        'fat': round((today_macros['fat'] / total_macros) * 100),
    }
    
    # Determine most and least consumed
    most_eaten_macro = max(macro_percentages, key=macro_percentages.get)
    least_eaten_macro = min(macro_percentages, key=macro_percentages.get)
    most_percentage = macro_percentages[most_eaten_macro]
    least_percentage = macro_percentages[least_eaten_macro]
    
    return render(request, 'meals/meal_log.html', {
     'form': form,
      'logs': today_logs,
      'total_calories': total_calories,
      'recommendation': recommendation,
      'weekly_data': weekly_data,
      'weekly_labels': json.dumps(weekly_labels),
      'weekly_calories': json.dumps(weekly_calories),
       'macro_percentages': macro_percentages,
        'most_eaten_macro': most_eaten_macro,
       'least_eaten_macro': least_eaten_macro,
       'most_percentage': most_percentage,
       'least_percentage': least_percentage,})