from rag_battle.domain.embeddings_model import BaseEmbeddingsModel


class MockEmbeddingsModel(BaseEmbeddingsModel):
    async def embed_queries(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 100] * len(texts)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 100] * len(texts)
