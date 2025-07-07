import time

import tenacity
from grpc import RpcError
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

    @staticmethod
    def is_retryable_grpc_error(exception: BaseException) -> bool:
        if isinstance(exception, RpcError):
            return exception.code().name in {
                "UNAVAILABLE",
                "DEADLINE_EXCEEDED",
                "RESOURCE_EXHAUSTED",
            }
        return False

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(5),
        wait=(
            # use exponential backoff to gradually increase delay between retries
            tenacity.wait_exponential(multiplier=0.5, min=0.1, max=1.0)
            # add jitter to prevent retry storm when many clients retry simultaneously
            + tenacity.wait_random(0, 1)
        ),
        retry=tenacity.retry_if_exception(is_retryable_grpc_error),
        reraise=True,
    )
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
