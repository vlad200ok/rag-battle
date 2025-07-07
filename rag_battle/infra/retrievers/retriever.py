import time
import numpy as np
from loguru import logger

from rag_battle.domain.schemas import RAGQuery
from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.vector_database import DataItemType


class Retriever(BaseRetriever):
    async def retrieve(self, query: RAGQuery) -> list[DataItemType]:
        calculate_embeddings_start_time = time.time()
        embeddings = await self._embeddings_model.embed_queries([query.query])
        calculate_embeddings_end_time = time.time()
        calculate_embeddings_execution_time = (
            calculate_embeddings_end_time - calculate_embeddings_start_time
        )
        logger.info(
            f"Calculate query embeddings execution time: "
            f"{calculate_embeddings_execution_time:.3f} s."
        )

        query_start_time = time.time()
        items = await self._vector_database.query(
            query_embeddings=[np.array(embedding) for embedding in embeddings],
            tags=query.tags,
            num_items=query.num_items,
            remove_duplicates=query.remove_duplicates,
        )
        query_end_time = time.time()
        logger.info(f"Query executing time: {query_end_time - query_start_time:.3f} s.")
        return items
