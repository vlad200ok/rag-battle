import time

from loguru import logger

from rag_battle.domain.embeddings_pipeline import EmbeddingsPipeline
from rag_battle.domain.vector_database import DataItemType


class DocumentIngestionService:
    """
    Service for ingesting documents into the RAG system.

    This service handles the document ingestion workflow, including performance
    monitoring and error handling. It uses the embeddings pipeline to process
    and store documents in the vector database.
    """

    def __init__(
        self,
        embeddings_pipeline: EmbeddingsPipeline,
    ):
        """
        Initialize the document ingestion service with required components.

        :param embeddings_pipeline: The pipeline that handles embedding and storage
        processes.
        """
        self._embeddings_pipeline = embeddings_pipeline

    async def ingest_documents(self, documents: list[DataItemType]) -> None:
        """
        Ingest documents into the RAG system.

        This method processes a batch of documents by generating their embeddings
        and storing them in the vector database. It measures and logs the execution
        time for performance monitoring.

        :param documents: List of documents to ingest into the system.

        :return: None: The documents are processed and stored as a side effect.
        """
        start_time = time.time()
        await self._embeddings_pipeline.embed_and_save(documents)
        end_time = time.time()
        logger.info(
            f"Document ingestion executing time: {end_time - start_time:.3f} s."
        )
