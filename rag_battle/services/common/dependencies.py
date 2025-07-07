from rag_battle.domain.embeddings_model import BaseEmbeddingsModel

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
