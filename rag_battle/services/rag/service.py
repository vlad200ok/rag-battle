from rag_battle.domain.retriever import BaseRetriever
from rag_battle.domain.schemas import RAGQuery


class RAGService:
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever

    async def query(self, query: RAGQuery) -> list[str]:
        docs = await self.retriever.retrieve(query=query)
        return docs
