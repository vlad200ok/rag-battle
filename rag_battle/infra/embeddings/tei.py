from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.infra.embeddings.text_embeddings_inference.embedding import (
    embeddings_grpc,
)
from rag_battle.infra.embeddings.service import Service


class TEIEmbeddingsModel(BaseEmbeddingsModel):
    def __init__(self, service: Service):
        self._service = service

    async def embed_queries(self, texts: list[str]) -> list[list[float]]:
        return await self._embed(texts)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return await self._embed(texts)

    async def _embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = await embeddings_grpc(
            texts,
            host=self._service.host,
            port=self._service.port,
        )
        return embeddings.tolist()
