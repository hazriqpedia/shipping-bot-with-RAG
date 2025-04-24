import os
import faiss
import pickle
from .base import VectorStore
import numpy as np  # make sure it's at the top

INDEX_PATH = "be/storage/faiss_index/index.faiss"
META_PATH = "be/storage/faiss_index/metadata.pkl"


class FAISSVectorStore(VectorStore):
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.metadata = []
        self.index = None
        self._load_index()

    def _load_index(self):
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(META_PATH, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def _save_index(self):
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    # async def add(self, text: str) -> str:
    #     if not isinstance(text, list):
    #         text = [text]

    #     # Embedding: Text -> Vector
    #     from be.core.embeddings.factory import EmbeddingFactory
    #     embedder = EmbeddingFactory.create_embedder()
    #     vector = embedder.embed(text)
    #     vector_np = np.array(vector)
    #     print('vector shape:', vector_np.shape)

    #     self.index.add(vector_np)
    #     self.metadata.append(text[0])
    #     self._save_index()
    #     return "Added"

    async def add(self, vector: list[float], text: str) -> str:
        vector_np = np.array([vector])
        self.index.add(vector_np)
        self.metadata.append(text)
        self._save_index()
        return "Added"


    async def update(self, id: str, text: str) -> str:
        idx = int(id)
        if idx >= len(self.metadata):
            return "Invalid ID"
        self.metadata[idx] = text
        await self.reindex(self.metadata)
        return "Updated"

    async def delete(self, id: str) -> str:
        idx = int(id)
        if idx >= len(self.metadata):
            return "Invalid ID"
        self.metadata.pop(idx)
        await self.reindex(self.metadata)
        return "Deleted"

    async def search(self, query_vector: list[float], k: int = 3) -> list[str]:
        query_vector_np = np.array([query_vector])
        D, I = self.index.search(query_vector_np, k)
        return [self.metadata[i] for i in I[0] if i < len(self.metadata)]

    async def reindex(self, vectors: list[list[float]], texts: list[str]) -> str:
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(vectors))
        self.metadata = texts
        self._save_index()
        return "Reindexed"

    async def list_all(self) -> list[dict]:
        return [{"id": str(i), "text": text} for i, text in enumerate(self.metadata)]
