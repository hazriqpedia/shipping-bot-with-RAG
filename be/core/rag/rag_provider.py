from be.core.embeddings.factory import EmbeddingFactory
from be.core.vectorstores.factory import VectorStoreFactory


class RAGProvider:
    def __init__(self):
        self.embedder = EmbeddingFactory.create_embedder()
        self.vectorstore = VectorStoreFactory.create_store()

    async def retrieve_context(self, query: str) -> str:
        query_vec = self.embedder.embed([query])[0]

        docs = await self.vectorstore.search(query_vec)
        return "\n\n".join(docs)

    async def add_context(self, text: str):
        # return await self.vectorstore.add(text)
        vector = self.embedder.embed([text])[0]
        return await self.vectorstore.add(vector, text)

    async def update_context(self, id: str, text: str):
        return await self.vectorstore.update(id, text)

    async def delete_context(self, id: str):
        return await self.vectorstore.delete(id)

    async def reindex_context(self):
        vectors = self.embedder.embed(self.vectorstore.metadata)
        return await self.vectorstore.reindex(vectors, self.vectorstore.metadata)
