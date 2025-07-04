from fastapi import Depends

from rag_battle.services.rag import RAGService
from rag_battle.infra.retrievers import BaseRetriever, MockRetriever
from rag_battle.infra.embeddings import BaseEmbeddingsModel, MockEmbeddingsModel


async def get_embeddings_model() -> BaseEmbeddingsModel:
    return MockEmbeddingsModel()


async def get_retriever(
    embeddings_model: BaseEmbeddingsModel = Depends(get_embeddings_model),
) -> BaseRetriever:
    return MockRetriever(embeddings_model)


async def get_rag_service(
    retriever=Depends(get_retriever),
) -> RAGService:
    return RAGService(
        retriever=retriever,
    )
