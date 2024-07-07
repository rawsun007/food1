import requests


def fetch_recipes(recipe_name, next_url=None):
    if next_url:
        api_url = next_url
        params = {}
    else:
        api_url = "https://api.edamam.com/search"
        params = {
            'q': recipe_name,
            'app_id': '14d58d9f',
            'app_key': '07ebe8a1b6aecfbc4d8fa2c6e1663b1b',
            'to': 3
        }

    response = requests.get(api_url, params=params)
    data = response.json()

    # Debug logging
    print("API URL:", api_url)
    print("Response Data:", data)

    recipes = data.get('hits', [])
    next_page_url = data.get('_links', {}).get('next', {}).get('href', None)

    return recipes, next_page_url
