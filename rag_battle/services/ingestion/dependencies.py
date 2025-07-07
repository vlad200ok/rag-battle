from fastapi import Depends

from rag_battle.services.ingestion import DocumentIngestionService

from rag_battle.domain.embeddings_pipeline import EmbeddingsPipeline
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel

from rag_battle.services.common.dependencies import (
    get_embeddings_model,
    VECTOR_DATABASE,
)


async def get_embeddings_pipeline(
    embeddings_model: BaseEmbeddingsModel = Depends(get_embeddings_model),
) -> EmbeddingsPipeline:
    return EmbeddingsPipeline(
        embeddings_model=embeddings_model, vector_database=VECTOR_DATABASE
    )


async def get_document_ingestion_service(
    embeddings_pipeline=Depends(get_embeddings_pipeline),
) -> DocumentIngestionService:
    return DocumentIngestionService(
        embeddings_pipeline=embeddings_pipeline,
    )
