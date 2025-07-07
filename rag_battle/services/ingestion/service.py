import time

from loguru import logger

from rag_battle.domain.embeddings_pipeline import EmbeddingsPipeline
from rag_battle.domain.vector_database import DataItemType


class DocumentIngestionService:
    def __init__(
        self,
        embeddings_pipeline: EmbeddingsPipeline,
    ):
        self._embeddings_pipeline = embeddings_pipeline

    async def ingest_documents(self, documents: list[DataItemType]) -> None:
        start_time = time.time()
        await self._embeddings_pipeline.embed_and_save(documents)
        end_time = time.time()
        logger.info(
            f"Document ingestion executing time: {end_time - start_time:.3f} s."
        )
