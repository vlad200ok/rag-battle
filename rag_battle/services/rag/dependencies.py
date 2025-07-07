from fastapi import Depends

from rag_battle.services.rag import RAGService

from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel

from rag_battle.infra.retrievers import Retriever
from rag_battle.services.common.dependencies import (
    get_embeddings_model,
    VECTOR_DATABASE,
)


async def get_retriever(
    embeddings_model: BaseEmbeddingsModel = Depends(get_embeddings_model),
) -> BaseRetriever:
    return Retriever(embeddings_model=embeddings_model, vector_database=VECTOR_DATABASE)


async def get_rag_service(
    retriever=Depends(get_retriever),
) -> RAGService:
    return RAGService(
        retriever=retriever,
    )
