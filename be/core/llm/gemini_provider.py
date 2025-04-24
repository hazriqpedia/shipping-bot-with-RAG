from .base import LLMProvider
from google import genai
from google.genai import types


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str):
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)

    async def generate_response(self, query: str):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=query
        )

        print('raw response', response)
        return response.text
