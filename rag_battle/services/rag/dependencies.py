from fastapi import Depends

from rag_battle.services.rag import RAGService

from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel

from rag_battle.infra.retrievers import Retriever
from rag_battle.infra.vector_database import FaissVectorDatabase
from rag_battle.infra.embeddings import TEIEmbeddingsModel
from rag_battle.infra.embeddings.service import TEIService
from rag_battle.infra.embeddings.tei import TEIEmbeddingsModelConfig


async def get_embeddings_model() -> BaseEmbeddingsModel:
    return TEIEmbeddingsModel(
        service=TEIService(),
        config=TEIEmbeddingsModelConfig(),
    )


# TODO: create better init
VECTOR_DATABASE = FaissVectorDatabase(
    embedding_size=TEIEmbeddingsModelConfig().embedding_size
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
