from fastapi import Depends

from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.embeddings_pipeline import EmbeddingsPipeline
from rag_battle.domain.vector_database import VectorDatabase

from rag_battle.infra.retrievers import Retriever
from rag_battle.services.ingestion import DocumentIngestionService

from rag_battle.services.rag import RAGService
from rag_battle.services.common.dependencies import (
    create_vector_database,
    get_embeddings_model,
)
from rag_battle.services.ingestion.dependencies import get_document_ingestion_service
from rag_battle.services.rag.dependencies import get_rag_service


async def override_dependencies(app):
    vector_database = create_vector_database()

    await override_get_rag_service(app, vector_database)
    await override_get_document_ingestion_service(app, vector_database)

    yield


async def override_get_rag_service(
    app,
    vector_database: VectorDatabase,
) -> None:

    async def get_test_retriever(
        embeddings_model: BaseEmbeddingsModel = Depends(get_embeddings_model),
    ) -> BaseRetriever:
        return Retriever(
            embeddings_model=embeddings_model, vector_database=vector_database
        )

    async def get_test_rag_service(
        retriever=Depends(get_test_retriever),
    ) -> RAGService:
        return RAGService(
            retriever=retriever,
        )

    app.dependency_overrides[get_rag_service] = get_test_rag_service


async def override_get_document_ingestion_service(
    app,
    vector_database: VectorDatabase,
) -> None:
    async def get_test_embeddings_pipeline(
        embeddings_model: BaseEmbeddingsModel = Depends(get_embeddings_model),
    ) -> EmbeddingsPipeline:
        return EmbeddingsPipeline(
            embeddings_model=embeddings_model, vector_database=vector_database
        )

    async def get_test_document_ingestion_service(
        embeddings_pipeline=Depends(get_test_embeddings_pipeline),
    ) -> DocumentIngestionService:
        return DocumentIngestionService(
            embeddings_pipeline=embeddings_pipeline,
        )

    app.dependency_overrides[get_document_ingestion_service] = (
        get_test_document_ingestion_service
    )
