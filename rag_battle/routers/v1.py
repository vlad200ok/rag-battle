from fastapi import APIRouter, Depends

from rag_battle.routers import schemas
from rag_battle.services.rag import RAGService, get_rag_service

router = APIRouter()


@router.post("/query")
async def query_api(
    query: schemas.RAGQuery,
    rag_service: RAGService = Depends(get_rag_service),
):
    return await rag_service.query(query.query)
