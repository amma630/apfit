import openai
import requests
import os
from django.shortcuts import render
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
USDA_API_KEY = os.getenv("USDA_API_KEY")

def get_usda_response(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": USDA_API_KEY,
        "query": query,
        "pageSize": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "foods" in data and data["foods"]:
            food = data["foods"][0]
            description = food["description"]
            nutrients = food.get("foodNutrients", [])
            nutrient_info = ""

            for nutrient in nutrients[:5]:
                nutrient_info += f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}<br>"

            return f"<strong>{description}</strong><br>{nutrient_info}"
    except Exception as e:
        print("USDA API failed:", e)

    return None

def get_openai_response(query):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a health and nutrition expert."},
                {"role": "user", "content": query}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return "Sorry, I'm having trouble accessing the AI right now."

def chat_view(request):
    query = None
    response = None

    if request.method == "POST":
        query = request.POST.get("query", "")
        image = request.FILES.get("image")

        # Optional: process image in future
        if image:
            query = "Image uploaded, image OCR not implemented yet."

        if query:
            usda_answer = get_usda_response(query)
            if usda_answer:
                response = usda_answer
            else:
                response = get_openai_response(query)

    return render(request, "ai_chat/chat.html", {"query": query, "response": response})
