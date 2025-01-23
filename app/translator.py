import requests
import os

class Translator:
    def __init__(self):
        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"
        self.api_key = os.getenv('TRANSLATOR_API_KEY', 'your_api_key_here')
        self.region = os.getenv('TRANSLATOR_REGION', 'your_region_here')

    def translate(self, text, target_language):
        if not text:
            raise ValueError("Text to translate cannot be empty.")
        if not target_language:
            raise ValueError("Target language must be specified.")

        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json'
        }
        params = {
            'api-version': '3.0',
            'to': target_language
        }
        body = [{
            'text': text
        }]

        response = requests.post(self.endpoint, headers=headers, params=params, json=body)

        if response.status_code == 200:
            translations = response.json()
            return translations[0]['translations'][0]['text']
        else:
            raise Exception(f"Translation API error: {response.status_code}, {response.text}")
