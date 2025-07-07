import time

from loguru import logger
from rag_battle.domain.embeddings_model import (
    BaseEmbeddingsModel,
    EmbeddingsModelConfigType,
)
from rag_battle.infra.embeddings.text_embeddings_inference.embedding import (
    embeddings_grpc,
)
from rag_battle.infra.embeddings.service import Service
from rag_battle.infra.embeddings.tei.config import TEIEmbeddingsModelConfig


class TEIEmbeddingsModel(BaseEmbeddingsModel[TEIEmbeddingsModelConfig]):
    def __init__(self, config: EmbeddingsModelConfigType, service: Service):
        super().__init__(config=config)
        self._service = service

    async def embed_queries(self, texts: list[str]) -> list[list[float]]:
        return await self._embed(texts)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return await self._embed(texts)

    async def _embed(self, texts: list[str]) -> list[list[float]]:
        start_time = time.time()
        embeddings = await embeddings_grpc(
            texts,
            host=self._service.host,
            port=self._service.port,
        )
        end_time = time.time()
        logger.info(
            f"{len(texts)} embeddings calculating time: {end_time - start_time:.3f} s."
        )
        return embeddings.tolist()
