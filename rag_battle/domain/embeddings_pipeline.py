import numpy as np

from rag_battle.domain.vector_database import VectorDatabase
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.domain.schemas import DataItemType, DataItemWithEmbedding


class EmbeddingsPipeline:
    """
    Pipeline for processing documents through embedding and storage.

    This class coordinates the process of converting document text into vector
    embeddings and storing them in the vector database. It acts as an orchestration
    layer between the embedding model and vector database components.
    """

    def __init__(
        self,
        vector_database: VectorDatabase,
        embeddings_model: BaseEmbeddingsModel,
    ):
        """
        Initialize the embeddings pipeline with required components.

        :param vector_database: The database for storing vector embeddings.
        :param embeddings_model: The model that generates embeddings.
        """
        self._vector_database = vector_database
        self._embeddings_model = embeddings_model

    async def embed_and_save(self, documents: list[DataItemType]) -> None:
        """
        Process documents by generating embeddings and saving to the vector database.

        This method extracts text content from documents, generates vector
        embeddings using the embedding model, and then stores both the original
        documents and their embeddings in the vector database.

        :param documents: List of documents to process and store.

        :return: None: The documents are saved to the vector database as a side effect.
        """
        documents_with_embeddings: list[DataItemWithEmbedding] = []
        texts: list[str] = []
        for document in documents:
            texts.append(document.content)
        embeddings = await self._embeddings_model.embed_documents(texts)
        for i in range(len(documents)):
            documents_with_embeddings.append(
                DataItemWithEmbedding(
                    item=documents[i],
                    embedding=np.array(embeddings[i]),
                )
            )
        await self._vector_database.save_items(documents_with_embeddings)
