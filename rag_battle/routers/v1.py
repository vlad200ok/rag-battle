import fastapi
from fastapi import APIRouter, Depends

from rag_battle.routers import schemas
from rag_battle.domain.schemas import RAGQuery, DataItem
from rag_battle.services.rag import RAGService, get_rag_service
from rag_battle.services.ingestion import (
    DocumentIngestionService,
    get_document_ingestion_service,
)
from rag_battle.domain.exceptions import InvalidInputException

router = APIRouter()


@router.post(
    "/query",
    response_model=schemas.RAGQueryResponseDTO,
    tags=["RAG"],
    summary="Search relevant documents",
    description=(
        "Given a user query and a list of tags, this endpoint performs a "
        "retrieval-augmented generation (RAG) search over a knowledge base and "
        "returns a list of top-ranked documents, optionally removing duplicates."
    ),
    status_code=fastapi.status.HTTP_200_OK,
    responses={
        fastapi.status.HTTP_200_OK: {
            "description": "Search results successfully returned.",
        },
        fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error – invalid input format.",
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error during document ingestion."
        },
    },
)
async def query_api(
    payload: schemas.RAGQueryDTO,
    rag_service: RAGService = Depends(get_rag_service),
) -> schemas.RAGQueryResponseDTO:
    query = RAGQuery(**payload.model_dump())
    try:
        items = await rag_service.query(query)
    except InvalidInputException as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during extracting relevant items.",
        )

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


@router.put(
    "/",
    response_model=None,
    tags=["RAG"],
    summary="Add documents to knowledge base",
    description=(
        "Ingests a batch of documents into the vector database. "
        "Each document includes an identifier, content, and associated tags. "
        "Duplicate IDs will overwrite existing entries with the same ID."
    ),
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
    responses={
        fastapi.status.HTTP_204_NO_CONTENT: {
            "description": "Documents successfully added to the knowledge base.",
        },
        fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error – invalid input format.",
        },
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error during document ingestion."
        },
    },
)
async def add_documents_api(
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
    try:
        await ingestion_service.ingest_documents(documents)
    except InvalidInputException as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during document ingestion.",
        )
