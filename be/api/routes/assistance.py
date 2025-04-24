from fastapi import APIRouter
from be.core.llm.base import LLMProvider
from be.core.rag.rag_provider import RAGProvider
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import time


class QueryRequest(BaseModel):
    query: str
    is_use_rag: bool = False


class LLMResponse(BaseModel):
    query: str
    response: str
    is_rag_enabled: bool
    context: Optional[str]
    provider: str
    llm_model: str
    query_time: datetime
    time_taken_ms: float


def get_router(llm_provider: LLMProvider, rag_provider: RAGProvider) -> APIRouter:
    router = APIRouter(prefix="/assistance", tags=["Assistance"])

    @router.post("/")
    async def get_response_from_assistance(request: QueryRequest):
        try:
            context = None
            user_query = request.query
            llm_query = query = (
                            f"You are an expert assistant.\n\n"
                            f"Answer the following question using your own knowledge.\n\n"
                            f"Question:\n{user_query}\n\n"
                            f"Answer:"
                        )
            is_use_rag = request.is_use_rag
            query_time = datetime.utcnow()
            start_time = time.perf_counter()

            # RAG (optional)
            if is_use_rag:
                context = await rag_provider.retrieve_context(query)
                print('context: ', context)
                if context:
                    llm_query = (
                                    f"You are an expert assistant.\n\n"
                                    f"If the context below is relevant, use it to answer the question.\n"
                                    f"If it's not helpful, answer using your own knowledge.\n\n"
                                    f"Context:\n{context}\n\n"
                                    f"Question:\n{query}\n\n"
                                    f"Answer:"
                                )

            # Calling LLM
            response = await llm_provider.generate_response(llm_query)
            time_taken = (time.perf_counter() - start_time) * 1000  # in ms

            return LLMResponse(
                query=llm_query,
                is_rag_enabled=is_use_rag,
                context=context,
                response=response,
                provider=llm_provider.__class__.__name__.replace(
                    "Provider", "").lower(),
                llm_model=getattr(llm_provider, "model_name", "unknown"),
                query_time=query_time,
                time_taken_ms=round(time_taken, 2)
            )
        except Exception as e:
            print('error: ', e)
            return {"error": str(e)}

    return router
