import requests
import openai

USDA_API_KEY = 'biN2dEIYgmDFbIieDfka2jsh5xzSUvp2uYPp0r3W'
OPENAI_API_KEY = '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'  # or use a free alternative

openai.api_key = OPENAI_API_KEY

def query_usda_api(query):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        'query': query,
        'api_key': USDA_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            first_item = data['foods'][0]
            return f"Name: {first_item['description']}\nCalories: {first_item.get('foodNutrients', [{}])[0].get('value', 'N/A')}"
    return None


def fallback_ai_response(query):
    # This is for OpenAI or similar fallback
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-3
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, I couldn't process your query right now."
