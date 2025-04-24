from fastapi import APIRouter
from be.core.rag.rag_provider import RAGProvider
from pydantic import BaseModel

router = APIRouter(prefix="/rag",  tags=["Rag"])


def get_router(rag_provider: RAGProvider):
    class RAGAdd(BaseModel):
        text: str

    class RAGUpdate(BaseModel):
        text: str

    @router.get("/")
    async def get_status():
        return {"status": "alive"}

    @router.post("/add")
    async def add_rag_entry(data: RAGAdd):
        result = await rag_provider.add_context(data.text)
        return {"status": result}

    @router.patch("/{id}")
    async def update_rag_entry(id: str, data: RAGUpdate):
        result = await rag_provider.update_context(id, data.text)
        return {"status": result}

    @router.delete("/{id}")
    async def delete_rag_entry(id: str):
        result = await rag_provider.delete_context(id)
        return {"status": result}

    @router.post("/reindex")
    async def reindex_rag():
        result = await rag_provider.reindex_context()
        return {"status": result}

    @router.get("/list")
    async def list_rag_data():
        data = await rag_provider.vectorstore.list_all()
        return {"total": len(data), "data": data}

    return router
