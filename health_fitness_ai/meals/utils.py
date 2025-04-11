import requests
from django.conf import settings

def get_usda_nutrition(food_name, quantity, unit):
    try:
        api_key = getattr(settings, "USDA_API_KEY", None)
        if not api_key:
            raise ValueError("USDA API key not configured in settings.py")

        search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        detail_url_base = "https://api.nal.usda.gov/fdc/v1/food/"

        # Step 1: Search for the food item
        search_response = requests.get(search_url, params={
            "query": food_name,
            "pageSize": 1,
            "api_key": api_key
        })
        search_response.raise_for_status()
        foods = search_response.json().get("foods", [])
        if not foods:
            return None

        # Step 2: Fetch food details
        fdc_id = foods[0]["fdcId"]
        detail_response = requests.get(f"{detail_url_base}{fdc_id}", params={"api_key": api_key})
        detail_response.raise_for_status()
        data = detail_response.json()

        nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        per_100g = 100  # default base reference

        for nutrient in data.get("foodNutrients", []):
            name = nutrient.get("nutrient", {}).get("name", "").lower()
            value = nutrient.get("amount", 0)
            unit_name = nutrient.get("nutrient", {}).get("unitName", "").lower()

            if 'energy' in name and 'kcal' in unit_name:
                nutrition['calories'] = value
            elif 'protein' in name:
                nutrition['protein'] = value
            elif 'carbohydrate' in name:
                nutrition['carbs'] = value
            elif 'total lipid' in name or 'fat' in name:
                nutrition['fat'] = value

        # Step 3: Adjust based on quantity and unit
        multiplier = 1.0
        if unit.lower() == 'grams':
            multiplier = quantity / per_100g
        elif unit.lower() == 'ml':
            multiplier = quantity / 100
        elif unit.lower() == 'pieces':
            multiplier = quantity  # assuming 1 piece = ~100g
        elif unit.lower() == 'cups':
            multiplier = quantity * 2  # 1 cup = ~200g
        elif unit.lower() == 'tablespoons':
            multiplier = quantity * 0.15
        elif unit.lower() == 'teaspoons':
            multiplier = quantity * 0.05

        for key in nutrition:
            nutrition[key] = round(nutrition[key] * multiplier, 2)

        return nutrition
    except Exception as e:
        print(f"Nutrition fetch error: {e}")
        return None
