import requests
import json
USDA_API_KEY = 'biN2dEIYgmDFbIieDfka2jsh5xzSUvp2uYPp0r3W'

def get_usda_nutrition(food_name):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": food_name,
        "api_key": USDA_API_KEY
    }
    response = requests.get(search_url, params=params)
    data = response.json()

    if data.get("foods"):
        fdc_id = data["foods"][0]["fdcId"]
        detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
        detail_response = requests.get(detail_url, params={"api_key": USDA_API_KEY})
        detail_data = detail_response.json()

        nutrients = detail_data.get("foodNutrients", [])
        result = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}

        for n in nutrients:
            name = n.get("nutrientName", "").lower()
            value = n.get("value", 0)
            if "energy" in name and n.get("unitName") == "KCAL":
                result["calories"] = value
            elif "protein" in name:
                result["protein"] = value
            elif "fat" in name:
                result["fat"] = value
            elif "carbohydrate" in name:
                result["carbs"] = value
        return result
    return None
