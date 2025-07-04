from rag_battle.infra.retrievers.base import BaseRetriever


class MockRetriever(BaseRetriever):
    async def retrieve(self, query: str) -> list[str]:
        await self._embeddings_model.embed(query)
        return [query] * 10
