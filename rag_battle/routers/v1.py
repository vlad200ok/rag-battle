from fastapi import APIRouter, Depends

from rag_battle.routers import schemas
from rag_battle.domain.schemas import RAGQuery
from rag_battle.services.rag import RAGService, get_rag_service

router = APIRouter()


@router.post("/query")
async def query_api(
    query: schemas.RAGQueryDTO,
    rag_service: RAGService = Depends(get_rag_service),
):
    service_query = RAGQuery(**query.model_dump())
    return await rag_service.query(service_query)
