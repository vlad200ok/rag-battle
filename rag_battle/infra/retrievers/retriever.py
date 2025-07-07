import numpy as np

from rag_battle.domain.schemas import RAGQuery
from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.vector_database import DataItemType


class Retriever(BaseRetriever):
    async def retrieve(self, query: RAGQuery) -> list[DataItemType]:
        embeddings = await self._embeddings_model.embed_queries([query.query])
        items = await self._vector_database.query(
            query_embeddings=[np.array(embedding) for embedding in embeddings],
            tags=query.tags,
            num_items=query.num_items,
            remove_duplicates=query.remove_duplicates,
        )
        return items
