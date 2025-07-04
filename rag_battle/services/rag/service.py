from rag_battle.infra.retrievers import BaseRetriever


class RAGService:
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever

    async def query(self, user_query: str) -> list[str]:
        docs = await self.retriever.retrieve(user_query)
        return docs
