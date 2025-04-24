import os

from .base import LLMProvider
from .anthropic_provider import AnthropicProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider


class LLMFactory:
    @staticmethod
    def create_provider(provider_name: str) -> LLMProvider:
        provider_name = provider_name.lower()

        match provider_name:
            case "openai":
                api_key = os.environ.get("OPENAI_API_KEY")
                llm_model = os.environ.get("OPENAI_MODEL_NAME", "gpt-4")

                check_api_key(api_key)

                return OpenAIProvider(api_key, llm_model)

            case "gemini":
                api_key = os.environ.get("GEMINI_API_KEY")
                llm_model = os.environ.get(
                    "GEMINI_MODEL_NAME", "gemini-2.0-flash")

                check_api_key(api_key)

                return GeminiProvider(api_key, llm_model)

            case "anthropic":
                api_key = os.environ.get("ANTHROPIC_API_KEY")
                llm_model = os.environ.get(
                    "ANTHROPIC_MODEL_NAME", "claude-3-opus-20240229")

                check_api_key(api_key)

                return AnthropicProvider(api_key, llm_model)
            case _:
                raise ValueError(f"Unknown LLM provider: {provider_name}")

    @staticmethod
    def create_provider_from_env() -> LLMProvider:
        provider_name = os.environ.get("LLM_PROVIDER", "gemini")
        return LLMFactory.create_provider(provider_name)


def check_api_key(api_key: str):
    if api_key:
        return True
    else:
        raise ValueError("Key not Provided. This is mandatory.")


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

    llm = LLMFactory.create_provider("gemini")
    print('llm: ', llm)
    LLMFactory.normal_method()
