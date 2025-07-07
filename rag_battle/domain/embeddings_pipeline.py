import numpy as np

from rag_battle.domain.vector_database import VectorDatabase
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.domain.schemas import DataItemType, DataItemWithEmbedding


class EmbeddingsPipeline:
    def __init__(
        self,
        vector_database: VectorDatabase,
        embeddings_model: BaseEmbeddingsModel,
    ):
        self._vector_database = vector_database
        self._embeddings_model = embeddings_model

    async def embed_and_save(self, documents: list[DataItemType]) -> None:
        documents_with_embeddings: list[DataItemWithEmbedding] = []
        texts: list[str] = []
        for document in documents:
            texts.append(document.content)
        embeddings = await self._embeddings_model.embed_documents(texts)
        for i in range(len(documents)):
            documents_with_embeddings.append(
                DataItemWithEmbedding(
                    item=documents[i],
                    embedding=np.array(embeddings[i]),
                )
            )
        await self._vector_database.save_items(documents_with_embeddings)
