from rag_battle.domain.retriever import BaseRetriever


class MockRetriever(BaseRetriever):
    async def retrieve(self, query: str) -> list[str]:
        await self._embeddings_model.embed(query)
        return [query] * 10
