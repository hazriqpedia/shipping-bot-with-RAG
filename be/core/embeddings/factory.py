import os
from .base import EmbeddingModel
from .sentence_transformer import SentenceTransformerEmbedding


class EmbeddingFactory:
    @staticmethod
    def create_embedder(provider_name: str = None) -> EmbeddingModel:
        provider = (provider_name or os.getenv(
            "EMBEDDING_PROVIDER", "sentence-transformer")).lower()

        match provider:
            case "sentence-transformer":
                return SentenceTransformerEmbedding()
            case _:
                raise ValueError(f"Unknown embedding provider: {provider}")
