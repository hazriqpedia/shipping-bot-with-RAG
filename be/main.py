from fastapi import FastAPI, APIRouter
from be.api.routes import assistance, rag
from be.core.llm.factory import LLMFactory
from be.core.rag.rag_provider import RAGProvider

app = FastAPI()

llm_provider = LLMFactory.create_provider_from_env()
rag_provider = RAGProvider()

api_routers = APIRouter(prefix="/api")
api_routers.include_router(assistance.get_router(llm_provider, rag_provider))
api_routers.include_router(rag.get_router(rag_provider))

app.include_router(api_routers)


@app.get("/")
def index():
    return {"status": "app is running..."}
