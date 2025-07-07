import time
from loguru import logger

from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.schemas import RAGQuery
from rag_battle.domain.vector_database import DataItemType


class RAGService:
    """
    Service for performing Retrieval-Augmented Generation (RAG) operations.

    This service handles RAG queries by using an injected retriever implementation
    that interfaces with vector databases and embedding models. It measures and logs
    query performance metrics.
    """

    def __init__(self, retriever: BaseRetriever):
        """
        Initialize the RAG service with a retriever implementation.

        :param retriever: The retrieval component that will perform
        semantic search operations.
        """
        self.retriever = retriever

    async def query(self, query: RAGQuery) -> list[DataItemType]:
        """
        Execute a RAG query to retrieve relevant documents.

        This method measures the execution time of the retrieval operation
        and logs it for performance monitoring.
        :param query: The query object containing the search text,
        filtering tags, and retrieval parameters.

        :return: list[DataItemType]: A list of retrieved documents that match the query,
        ordered by relevance.
        """
        start_time = time.time()
        docs = await self.retriever.retrieve(query=query)
        end_time = time.time()
        logger.info(f"RAG query executing time: {end_time - start_time:.3f} s.")
        return docs
