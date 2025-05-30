# app/services/quote_service.py

import requests
from flask import current_app

def get_random_quote():
    api_url = 'https://api.api-ninjas.com/v1/quotes'
    try:
        api_key = current_app.config.get('API_NINJAS_KEY')
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        return f"Ошибка получения цитаты: {e}"