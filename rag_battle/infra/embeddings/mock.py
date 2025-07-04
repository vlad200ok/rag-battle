from rag_battle.infra.embeddings.base import BaseEmbeddingsModel


class MockEmbeddingsModel(BaseEmbeddingsModel):
    async def embed(self, text: str) -> list[float]:
        return [0.0] * 100
