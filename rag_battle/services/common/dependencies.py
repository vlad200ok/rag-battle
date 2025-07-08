from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.domain.vector_database import VectorDatabase

from rag_battle.infra.vector_database import FaissVectorDatabase
from rag_battle.infra.embeddings import TEIEmbeddingsModel
from rag_battle.infra.embeddings.service import TEIService
from rag_battle.infra.embeddings.tei import TEIEmbeddingsModelConfig


async def get_embeddings_model() -> BaseEmbeddingsModel:
    return TEIEmbeddingsModel(
        service=TEIService(),
        config=TEIEmbeddingsModelConfig(),
    )


def create_vector_database() -> VectorDatabase:
    return FaissVectorDatabase(
        embedding_size=TEIEmbeddingsModelConfig().embedding_size,
    )


VECTOR_DATABASE = create_vector_database()
