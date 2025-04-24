from abc import ABC, abstractmethod


class LLMProvider(ABC):
    def __init__(self, api_key: str, api_model: str, **kwargs):
        print('api key: ', api_key)
        pass

    @abstractmethod
    async def generate_response(self, query: str):
        pass
