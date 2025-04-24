from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    async def add(self, text: str) -> str:
        pass

    @abstractmethod
    async def update(self, id: str, text: str) -> str:
        pass

    @abstractmethod
    async def delete(self, id: str) -> str:
        pass

    @abstractmethod
    async def search(self, query_vector: list[float], k: int = 3) -> list[str]:
        pass

    @abstractmethod
    async def reindex(self, texts: list[str]) -> str:
        pass

    @abstractmethod
    async def list_all(self) -> list[dict]:
        """
        Returns a list of all documents in the vector store.
        """
        pass
