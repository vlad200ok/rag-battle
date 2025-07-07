from fastapi import APIRouter, Depends

from rag_battle.routers import schemas
from rag_battle.domain.schemas import RAGQuery, DataItem
from rag_battle.services.rag import RAGService, get_rag_service
from rag_battle.services.ingestion import (
    DocumentIngestionService,
    get_document_ingestion_service,
)

router = APIRouter()


@router.post("/query", response_model=schemas.RAGQueryResponseDTO)
async def query_api(
    payload: schemas.RAGQueryDTO,
    rag_service: RAGService = Depends(get_rag_service),
) -> schemas.RAGQueryResponseDTO:
    query = RAGQuery(**payload.model_dump())
    items = await rag_service.query(query)

    dto_items: list[schemas.DocumentWithScoreDTO] = []
    for item in items:
        dto_items.append(
            schemas.DocumentWithScoreDTO(
                item_id=item.item_id,
                content=item.content,
                tags=item.tags,
                score=item.score,
            )
        )

    return schemas.RAGQueryResponseDTO(items=dto_items)


@router.put("/", response_model=None)
async def add_documents(
    payload: schemas.RAGAddDocumentsDTO,
    ingestion_service: DocumentIngestionService = Depends(
        get_document_ingestion_service
    ),
) -> None:
    documents: list[DataItem] = []
    for item in payload.documents:
        documents.append(
            DataItem(**item.model_dump()),
        )
    await ingestion_service.ingest_documents(documents)
