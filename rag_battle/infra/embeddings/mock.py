from rag_battle.domain.embeddings_model import BaseEmbeddingsModel


class MockEmbeddingsModel(BaseEmbeddingsModel):
    async def embed(self, text: str) -> list[float]:
        return [0.0] * 100
