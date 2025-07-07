import time
from loguru import logger

from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.schemas import RAGQuery
from rag_battle.domain.vector_database import DataItemType


class RAGService:
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever

    async def query(self, query: RAGQuery) -> list[DataItemType]:
        start_time = time.time()
        docs = await self.retriever.retrieve(query=query)
        end_time = time.time()
        logger.info(f"RAG query executing time: {end_time - start_time:.3f} s.")
        return docs
