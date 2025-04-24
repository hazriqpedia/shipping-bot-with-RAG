import os
from .base import VectorStore
from .faiss_store import FAISSVectorStore


class VectorStoreFactory:
    @staticmethod
    def create_store(provider_name: str = None) -> VectorStore:
        provider = (provider_name or os.getenv(
            "VECTORSTORE_PROVIDER", "faiss")).lower()

        match provider:
            case "faiss":
                return FAISSVectorStore()
            case _:
                raise ValueError(f"Unknown vector store: {provider}")
