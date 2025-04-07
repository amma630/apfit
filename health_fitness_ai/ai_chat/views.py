# ai_chat/views.py
from django.shortcuts import render
import requests

def chat_view(request):
    chat_history = []

    if request.method == "POST":
        question = request.POST.get('question')
        response = "Sorry, I couldn't find info."

        if question:
            # Search USDA Food Data Central API
            api_key = "YOUR_USDA_API_KEY"
            search_url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
            params = {
                "query": question,
                "api_key": api_key,
                "pageSize": 1
            }

            usda_response = requests.get(search_url, params=params)
            if usda_response.status_code == 200:
                data = usda_response.json()
                if data.get('foods'):
                    food = data['foods'][0]
                    description = food.get('description', 'No description')
                    calories = food.get('foodNutrients', [{}])[0].get('value', 'Unknown')
                    response = f"{description}: Approx. {calories} calories per 100g."
                else:
                    response = "No food data found."

            chat_history.append({'question': question, 'response': response})

    return render(request, 'ai_chat/chat.html', {'chat_history': chat_history})
